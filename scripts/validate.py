#!/usr/bin/env python3
"""Validate monthly paper submissions (Python 3.9+)."""
from datetime import date, datetime, timezone
import json
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import urlparse
from zoneinfo import ZoneInfo

import yaml

ROOT = Path(__file__).resolve().parents[1]


def title_key(value):
    """Match titles by Unicode-normalized words, retaining meaningful symbols."""
    value = unicodedata.normalize("NFKC", value).casefold()
    value = "".join(" " if unicodedata.category(c).startswith("P") else c for c in value)
    value = " ".join(value.split())
    if not any(c.isalnum() for c in value):
        raise ValueError("title must contain letters or numbers")
    return value


def timestamp(value):
    if not isinstance(value, str):
        raise ValueError("timestamp must be a quoted ISO 8601 string")
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None:
        raise ValueError("timestamp must include a timezone")
    return result


def validate_paper(meta, path, root, config, ledger, now):
    if not isinstance(meta, dict):
        raise ValueError("each paper must be a mapping")
    allowed = {"title", "url", "year", "venue", "topics", "code_url"}
    if set(meta) - allowed:
        raise ValueError(f"unknown metadata fields: {sorted(set(meta) - allowed)}")
    for key in ("title", "url"):
        if not isinstance(meta.get(key), str) or not meta[key].strip():
            raise ValueError(f"{key} must be a nonempty string")
    for key in ("url", "code_url"):
        if key in meta and (not isinstance(meta[key], str) or urlparse(meta[key]).scheme not in ("https", "http") or not urlparse(meta[key]).netloc):
            raise ValueError(f"{key} must be an absolute HTTP(S) URL")
    if type(meta.get("year")) is not int or not 1900 <= meta["year"] <= 2100:
        raise ValueError("year must be an integer between 1900 and 2100")
    if "venue" in meta and not isinstance(meta["venue"], str):
        raise ValueError("venue must be a string")
    topics = meta.get("topics", [])
    if not isinstance(topics, list) or not 0 <= len(topics) <= 3 or any(not isinstance(t, str) or t not in config["topics"] for t in topics):
        raise ValueError("topics must contain 0–3 IDs from config/paperlist.json")
    if len(set(topics)) != len(topics):
        raise ValueError("topics must not contain duplicates")
    if meta["title"].startswith("Replace with"):
        raise ValueError("replace the template title")
    member = path.parent.name
    if member not in config["members"]:
        raise ValueError(f"unknown member '{member}'; add them to config/paperlist.json")
    key = title_key(meta["title"])
    identity = f"{member}/title:{key}"
    added = ledger.get(identity, now)
    timestamp(added)
    return dict(meta, topics=topics, title_key=key, id=identity, member=member,
                member_name=config["members"][member],
                added_at=added,
                source=path.relative_to(root).as_posix())


def load_monthly(path, root, config, ledger, now):
    if not re.fullmatch(r"\d{4}-\d{2}", path.stem):
        raise ValueError("monthly filename must be YYYY-MM.yaml, e.g. 2026-10.yaml")
    year, month = path.stem.split("-")
    date(int(year), int(month), 1)
    batch = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(batch, dict) or set(batch) != {"papers"}:
        raise ValueError("monthly file must contain only a top-level 'papers' list")
    if not isinstance(batch["papers"], list) or not batch["papers"]:
        raise ValueError("papers must be a nonempty list")
    result = []
    for index, meta in enumerate(batch["papers"], start=1):
        try:
            note = validate_paper(meta, path, root, config, ledger, now)
            note["file_month"] = path.stem
            result.append(note)
        except (ValueError, TypeError) as exc:
            raise ValueError(f"papers[{index}]: {exc}") from exc
    return result


def collect(root, now=None):
    config = json.loads((root / "config/paperlist.json").read_text())
    ZoneInfo(config["timezone"])
    ledger = json.loads((root / "data/added_at.json").read_text())
    if not isinstance(ledger, dict):
        raise ValueError("data/added_at.json must be an object")
    for value in ledger.values():
        timestamp(value)
    now = now or datetime.now(timezone.utc).isoformat()
    entries, errors, seen = [], [], set()
    batches = set()
    for path in sorted((root / "entries").rglob("*")):
        if path.is_dir() or path.name == ".gitkeep":
            continue
        try:
            if path.is_symlink() or not path.is_file() or len(path.relative_to(root / "entries").parts) != 2:
                raise ValueError("submissions must be regular files at <member>/YYYY-MM.yaml")
            if path.suffix not in (".yaml", ".yml"):
                raise ValueError("only monthly YAML submissions are supported")
            batch_key = (path.parent.name, path.stem)
            if batch_key in batches:
                raise ValueError("only one monthly YAML file per member and month is allowed")
            batches.add(batch_key)
            for note in load_monthly(path, root, config, ledger, now):
                if note["id"] in seen:
                    raise ValueError(f"duplicate paper for this member: {note['title']} (including across months)")
                seen.add(note["id"])
                entries.append(note)
        except (ValueError, TypeError, yaml.YAMLError) as exc:
            errors.append(f"{path.relative_to(root)}: {exc}")
    if errors:
        raise ValueError("\n".join(errors))
    return config, ledger, sorted(entries, key=lambda n: timestamp(n["added_at"]), reverse=True)


if __name__ == "__main__":
    try:
        print(f"Validated {len(collect(ROOT)[2])} paper submissions.")
    except (ValueError, KeyError, OSError) as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        sys.exit(1)
