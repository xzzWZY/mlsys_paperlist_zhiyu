#!/usr/bin/env python3
"""Validate reading notes and build a portable static site (Python 3.9+)."""
import argparse
import hashlib
from datetime import date, datetime, timezone
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlparse
from zoneinfo import ZoneInfo

import yaml

ROOT = Path(__file__).resolve().parents[1]


def canonical_id(value):
    if not isinstance(value, str):
        raise ValueError("paper_id must be a string")
    value = value.strip().lower()
    if re.fullmatch(r"arxiv:(?:\d{4}\.\d{4,5}|[a-z.-]+/\d{7})(?:v\d+)?", value):
        return re.sub(r"v\d+$", "", value)
    if re.fullmatch(r"doi:10\.\d{4,9}/\S+", value):
        return value
    raise ValueError("paper_id must be arxiv:<identifier> or doi:<identifier>")


def timestamp(value):
    if not isinstance(value, str):
        raise ValueError("timestamp must be a quoted ISO 8601 string")
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None:
        raise ValueError("timestamp must include a timezone")
    return result


def week_of(value, tz):
    year, week, _ = timestamp(value).astimezone(ZoneInfo(tz)).isocalendar()
    return f"{year}-W{week:02d}"


def load_note(path, root, config, ledger, now, example=False):
    text = path.read_text(encoding="utf-8")
    match = re.fullmatch(r"---\r?\n(.*?)\r?\n---(?:\r?\n(.*))?", text, re.S)
    if not match:
        raise ValueError("expected YAML front matter between --- lines")
    return validate_paper(yaml.safe_load(match[1]), path, root, config, ledger, now, example)


def validate_paper(meta, path, root, config, ledger, now, example=False):
    if not isinstance(meta, dict):
        raise ValueError("front matter must be a mapping")
    allowed = {"paper_id", "title", "url", "year", "venue", "topics", "code_url"}
    if example:
        allowed.add("example_added_at")
    if set(meta) - allowed:
        raise ValueError(f"unknown metadata fields: {sorted(set(meta) - allowed)}")
    for key in ("paper_id", "title", "url"):
        if not isinstance(meta.get(key), str) or not meta[key].strip():
            raise ValueError(f"{key} must be a nonempty string")
    for key in ("url", "code_url"):
        if key in meta and (not isinstance(meta[key], str) or urlparse(meta[key]).scheme not in ("https", "http") or not urlparse(meta[key]).netloc):
            raise ValueError(f"{key} must be an absolute HTTP(S) URL")
    if type(meta.get("year")) is not int or not 1900 <= meta["year"] <= 2100:
        raise ValueError("year must be an integer between 1900 and 2100")
    if "venue" in meta and not isinstance(meta["venue"], str):
        raise ValueError("venue must be a string")
    topics = meta.get("topics")
    if not isinstance(topics, list) or not 1 <= len(topics) <= 3 or any(not isinstance(t, str) or t not in config["topics"] for t in topics):
        raise ValueError("topics must contain 1–3 IDs from config/site.json")
    if len(set(topics)) != len(topics):
        raise ValueError("topics must not contain duplicates")
    if meta["title"].startswith("Replace with"):
        raise ValueError("replace the template title")
    member = path.parent.name
    if not example and member not in config["members"]:
        raise ValueError(f"unknown member '{member}'; add them to config/site.json")
    paper_id = canonical_id(meta["paper_id"])
    identity = f"{member}/{paper_id}"
    added = meta.get("example_added_at") if example else ledger.get(identity, now)
    timestamp(added)
    return dict(meta, paper_id=paper_id, id=identity, member=member,
                member_name="Example reader" if example else config["members"][member],
                added_at=added, week=week_of(added, config["timezone"]),
                pending=not example and identity not in ledger, example=example,
                source=path.relative_to(root).as_posix())


def load_weekly(path, root, config, ledger, now, example=False):
    if not re.fullmatch(r"\d{4}-W\d{2}", path.stem):
        raise ValueError("weekly filename must be YYYY-Www.yaml, e.g. 2026-W41.yaml")
    year, week = path.stem.split("-W")
    date.fromisocalendar(int(year), int(week), 1)
    batch = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(batch, dict) or set(batch) != {"papers"}:
        raise ValueError("weekly file must contain only a top-level 'papers' list")
    if not isinstance(batch["papers"], list) or not batch["papers"]:
        raise ValueError("papers must be a nonempty list")
    result = []
    for index, meta in enumerate(batch["papers"], start=1):
        try:
            note = validate_paper(meta, path, root, config, ledger, now, example)
            note["file_week"] = path.stem
            result.append(note)
        except (ValueError, TypeError) as exc:
            raise ValueError(f"papers[{index}]: {exc}") from exc
    return result


def collect(root, now=None):
    config = json.loads((root / "config/site.json").read_text())
    ZoneInfo(config["timezone"])
    if type(config["weekly_target"]) is not int or config["weekly_target"] < 1:
        raise ValueError("weekly_target must be a positive integer")
    ledger = json.loads((root / "data/added_at.json").read_text())
    if not isinstance(ledger, dict):
        raise ValueError("data/added_at.json must be an object")
    for value in ledger.values():
        timestamp(value)
    now = now or datetime.now(timezone.utc).isoformat()
    entries, errors, seen = [], [], set()
    for folder, example in (("entries", False), ("examples", True)):
        batches = set()
        paths = sorted(p for p in (root / folder).rglob("*") if p.suffix in (".yaml", ".yml", ".md"))
        for path in paths:
            try:
                if path.is_symlink() or not path.is_file() or len(path.relative_to(root / folder).parts) != 2:
                    raise ValueError("submissions must be regular files at <member>/YYYY-Www.yaml")
                if path.suffix == ".md":
                    batch = [load_note(path, root, config, ledger, now, example)]
                else:
                    batch_key = (path.parent.name, path.stem)
                    if batch_key in batches:
                        raise ValueError("only one weekly YAML file per member and week is allowed")
                    batches.add(batch_key)
                    batch = load_weekly(path, root, config, ledger, now, example)
                for note in batch:
                    key = (example, note["id"])
                    if key in seen:
                        raise ValueError(f"duplicate paper for this member: {note['paper_id']} (including across weeks)")
                    seen.add(key)
                    entries.append(note)
            except (ValueError, TypeError, yaml.YAMLError) as exc:
                errors.append(f"{path.relative_to(root)}: {exc}")
    if errors:
        raise ValueError("\n".join(errors))
    return config, ledger, sorted(entries, key=lambda n: timestamp(n["added_at"]), reverse=True)


def build(root=ROOT, record=False, check=False):
    config, ledger, notes = collect(root)
    if check:
        print(f"Validated {len(notes)} notes (including examples).")
        return
    if record:
        for note in notes:
            if not note["example"]:
                ledger.setdefault(note["id"], note["added_at"])
                note["pending"] = False
        ledger_path = root / "data/added_at.json"
        temp = ledger_path.with_suffix(".tmp")
        temp.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n")
        temp.replace(ledger_path)
    dist = root / "dist"
    dist.mkdir(exist_ok=True)
    payload = {"config": config, "notes": notes}
    assets = {name: (root / "site" / name).read_bytes() for name in ("styles.css", "app.js")}
    assets["data.js"] = ("window.PAPERLIST = " + json.dumps(payload, ensure_ascii=True).replace("<", "\\u003c") + ";\n").encode("utf-8")
    page = (root / "site/index.html").read_text(encoding="utf-8")
    for name, content in assets.items():
        version = hashlib.sha256(content).hexdigest()[:16]
        path = Path(name)
        filename = f"{path.stem}.{version}{path.suffix}"
        (dist / filename).write_bytes(content)
        page = page.replace(f'./{name}', f'./{filename}')
    (dist / "index.html").write_text(page, encoding="utf-8")
    (dist / ".nojekyll").touch()
    print(f"Built {len(notes)} notes → {dist}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate without writing files")
    parser.add_argument("--record", action="store_true", help="Persist first-seen times (publishing only)")
    args = parser.parse_args()
    try:
        build(record=args.record, check=args.check)
    except (ValueError, KeyError, OSError) as exc:
        print(f"Build failed: {exc}", file=sys.stderr)
        sys.exit(1)
