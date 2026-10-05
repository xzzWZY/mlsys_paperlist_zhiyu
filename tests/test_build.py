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
        self.text = (ROOT / "examples/demo-reader/pagedattention.md").read_text()
        self.text = "\n".join(line for line in self.text.splitlines() if not line.startswith("example_added_at:")) + "\n"

    def add_note(self, text=None, name="paper.md"):
        path = self.member_dir / name
        path.write_text(text or self.text)
        return path

    def test_empty_library_and_examples_are_valid(self):
        self.assertEqual(builder.collect(self.root)[2], [])
        shutil.copytree(ROOT / "examples", self.root / "examples")
        notes = builder.collect(self.root)[2]
        self.assertEqual(len(notes), 2)
        self.assertTrue(all(n["example"] for n in notes))

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
            (ROOT / "templates/paper.md").read_text(),
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

    def test_invalid_ledger_is_not_silently_overwritten(self):
        (self.root / "data/added_at.json").write_text('{"bad": "2026-01-01"}')
        with self.assertRaisesRegex(ValueError, "timezone"):
            builder.collect(self.root)


if __name__ == "__main__":
    unittest.main()
