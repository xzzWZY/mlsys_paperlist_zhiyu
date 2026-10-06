import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("builder", ROOT / "scripts/build.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class BuildTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for directory in ("config", "data", "site"):
            shutil.copytree(ROOT / directory, self.root / directory)
        (self.root / "data/added_at.json").write_text("{}\n")
        self.member_dir = self.root / "entries/xzzWZY"
        self.member_dir.mkdir(parents=True)
        self.text = '\n'.join([
            '---', 'paper_id: "arxiv:2309.06180"', 'title: "PagedAttention"',
            'url: "https://arxiv.org/abs/2309.06180"', 'year: 2023',
            'topics: [llm-inference]', '---', ''
        ])

    def add_note(self, text=None, name="paper.md"):
        path = self.member_dir / name
        path.write_text(text or self.text)
        return path

    def test_empty_library_and_demo_entries_are_valid(self):
        self.assertEqual(builder.collect(self.root)[2], [])
        shutil.copytree(ROOT / "entries", self.root / "entries", dirs_exist_ok=True)
        notes = builder.collect(self.root)[2]
        self.assertEqual(len(notes), 6)
        self.assertTrue(all(not n["example"] for n in notes))

    def test_week_uses_chicago_and_iso_year(self):
        self.assertEqual(builder.week_of("2026-10-05T02:00:00Z", "America/Chicago"), "2026-W40")
        self.assertEqual(builder.week_of("2026-10-05T06:00:00Z", "America/Chicago"), "2026-W41")
        self.assertEqual(builder.week_of("2021-01-01T18:00:00Z", "America/Chicago"), "2020-W53")

    def test_stable_timestamp_after_edit_rename_and_readdition(self):
        path = self.add_note()
        builder.build(self.root, record=True)
        ledger = json.loads((self.root / "data/added_at.json").read_text())
        first = ledger["xzzWZY/arxiv:2309.06180"]
        path.write_text(self.text + "\nAn updated reading note.\n")
        path.rename(self.member_dir / "renamed.md")
        note = builder.collect(self.root, now="2027-01-01T00:00:00Z")[2][0]
        self.assertEqual(note["added_at"], first)
        self.assertFalse(note["pending"])
        (self.member_dir / "renamed.md").unlink()
        builder.build(self.root, record=True)
        self.add_note()
        self.assertEqual(builder.collect(self.root)[2][0]["added_at"], first)

    def test_local_preview_does_not_write_ledger(self):
        self.add_note()
        builder.build(self.root)
        self.assertEqual(json.loads((self.root / "data/added_at.json").read_text()), {})
        self.assertTrue(builder.collect(self.root)[2][0]["pending"])

    def test_duplicate_arxiv_versions_rejected(self):
        self.add_note()
        self.add_note(self.text.replace('paper_id: "arxiv:2309.06180"', 'paper_id: "arxiv:2309.06180v2"'), "duplicate.md")
        with self.assertRaisesRegex(ValueError, "duplicate paper"):
            builder.collect(self.root)

    def test_different_members_can_read_same_paper(self):
        self.add_note()
        config = json.loads((self.root / "config/site.json").read_text())
        config["members"]["second-reader"] = "Second reader"
        (self.root / "config/site.json").write_text(json.dumps(config))
        other = self.root / "entries/second-reader"
        other.mkdir()
        (other / "same-paper.md").write_text(self.text)
        self.assertEqual(len(builder.collect(self.root)[2]), 2)

    def test_invalid_content_fails_without_partial_recording(self):
        cases = [
            self.text.replace("llm-inference", "unknown-topic"),
            self.text.replace("https://arxiv.org/abs/2309.06180", "javascript:alert(1)"),
            self.text.replace("year: 2023", "year: true"),
            self.text.replace("year: 2023", 'year: 2023\nadded_at: "2020-01-01"'),
            self.text.replace("PagedAttention", "Replace with the full paper title"),
        ]
        for content in cases:
            with self.subTest(content=content[:100]):
                self.add_note(content)
                with self.assertRaises(ValueError):
                    builder.build(self.root, record=True)
                self.assertEqual(json.loads((self.root / "data/added_at.json").read_text()), {})

    def test_unknown_member_rejected(self):
        self.add_note()
        self.member_dir.rename(self.member_dir.with_name("unregistered"))
        with self.assertRaisesRegex(ValueError, "unknown member"):
            builder.collect(self.root)

    def test_metadata_only_and_legacy_body(self):
        self.add_note(self.text.rstrip())
        note = builder.collect(self.root)[2][0]
        self.assertEqual(note["paper_id"], "arxiv:2309.06180")
        self.add_note(self.text + "\n## Summary\n<script>legacy text</script>\n")
        note = builder.collect(self.root)[2][0]
        for field in ("summary", "body", "html"):
            self.assertNotIn(field, note)

    def test_asset_urls_change_when_content_changes(self):
        import re
        builder.build(self.root)
        first = (self.root / "dist/index.html").read_text()
        urls = re.findall(r'(?:src|href)="\./([^\"]+)"', first)
        self.assertEqual(len(urls), 3)
        for url in urls:
            self.assertTrue((self.root / "dist" / url).is_file())
        app = self.root / "site/app.js"
        app.write_text(app.read_text() + "\n// Updated version\n")
        builder.build(self.root)
        second = (self.root / "dist/index.html").read_text()
        self.assertNotEqual(first, second)
        self.assertNotIn('src="./app.js"', second)
        self.assertNotIn('src="./data.js"', second)

    def monthly(self, name="2026-10.yaml", papers=None):
        import yaml
        paper = yaml.safe_load(self.text.split("---")[1])
        path = self.member_dir / name
        path.write_text(yaml.safe_dump({"papers": papers if papers is not None else [paper]}))
        return path

    def test_monthly_append_and_migration_keep_existing_dates(self):
        import yaml
        old = self.add_note()
        builder.build(self.root, record=True)
        original = builder.collect(self.root)[2][0]["added_at"]
        old.unlink()
        path = self.monthly()
        paper = yaml.safe_load(path.read_text())["papers"][0]
        second = dict(paper, paper_id="arxiv:2205.14135", title="FlashAttention")
        self.monthly(papers=[paper, second])
        notes = builder.collect(self.root, now="2027-01-04T18:00:00Z")[2]
        by_id = {n["paper_id"]: n for n in notes}
        self.assertEqual(by_id["arxiv:2309.06180"]["added_at"], original)
        self.assertEqual(by_id["arxiv:2205.14135"]["week"], "2027-W01")
        self.assertEqual(by_id["arxiv:2205.14135"]["file_month"], "2026-10")

    def test_duplicate_across_monthly_files_rejected(self):
        self.monthly()
        self.monthly("2026-11.yaml")
        with self.assertRaisesRegex(ValueError, "duplicate paper"):
            builder.collect(self.root)

    def test_one_file_per_member_week(self):
        self.monthly()
        self.monthly("2026-10.yml")
        with self.assertRaisesRegex(ValueError, "one monthly YAML"):
            builder.collect(self.root)

    def test_monthly_invalid_shape_and_week(self):
        for filename, content in [
            ("2026-13.yaml", "papers: []"),
            ("2026-00.yaml", "papers: []"),
            ("week41.yaml", "papers: []"),
            ("2026-10.yaml", "papers: []"),
            ("2026-10.yaml", "papers: wrong"),
            ("2026-10.yaml", "papers: [null]"),
        ]:
            path = self.member_dir / filename
            path.write_text(content)
            with self.subTest(filename=filename, content=content):
                with self.assertRaises(ValueError):
                    builder.build(self.root, record=True)
                self.assertEqual(json.loads((self.root / "data/added_at.json").read_text()), {})
            path.unlink()

    def test_invalid_ledger_is_not_silently_overwritten(self):
        (self.root / "data/added_at.json").write_text('{"bad": "2026-01-01"}')
        with self.assertRaisesRegex(ValueError, "timezone"):
            builder.collect(self.root)


if __name__ == "__main__":
    unittest.main()
