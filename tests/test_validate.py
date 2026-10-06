import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("builder", ROOT / "scripts/validate.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for directory in ("config", "data"):
            shutil.copytree(ROOT / directory, self.root / directory)
        (self.root / "data/added_at.json").write_text("{}\n")
        self.member_dir = self.root / "entries/Zhiyu_Wu"
        self.member_dir.mkdir(parents=True)
        self.text = '\n'.join([
            '---', 'paper_id: "arxiv:2309.06180"', 'title: "PagedAttention"',
            'url: "https://arxiv.org/abs/2309.06180"', 'year: 2023',
            'topics: [llm-inference]', '---', ''
        ])


    def test_empty_library_and_demo_entries_are_valid(self):
        self.assertEqual(builder.collect(self.root)[2], [])
        shutil.copytree(ROOT / "entries", self.root / "entries", dirs_exist_ok=True)
        notes = builder.collect(self.root)[2]
        self.assertEqual(len(notes), 6)

    def monthly(self, name="2026-10.yaml", papers=None):
        import yaml
        paper = yaml.safe_load(self.text.split("---")[1])
        path = self.member_dir / name
        path.write_text(yaml.safe_dump({"papers": papers if papers is not None else [paper]}))
        return path


    def test_arxiv_versions_are_duplicates(self):
        import yaml
        paper = yaml.safe_load(self.text.split("---")[1])
        self.monthly(papers=[paper, dict(paper, paper_id="arxiv:2309.06180v2")])
        with self.assertRaisesRegex(ValueError, "duplicate paper"):
            builder.collect(self.root)

    def test_legacy_markdown_is_rejected(self):
        (self.member_dir / "paper.md").write_text(self.text)
        with self.assertRaisesRegex(ValueError, "only monthly YAML"):
            builder.collect(self.root)

    def test_unknown_topics_and_members_rejected(self):
        path = self.monthly()
        path.write_text(path.read_text().replace("llm-inference", "unknown"))
        with self.assertRaisesRegex(ValueError, "topics"):
            builder.collect(self.root)
        self.monthly()
        self.member_dir.rename(self.member_dir.with_name("unknown"))
        with self.assertRaisesRegex(ValueError, "unknown member"):
            builder.collect(self.root)

    def test_duplicate_across_monthly_files_rejected(self):
        self.monthly()
        self.monthly("2026-11.yaml")
        with self.assertRaisesRegex(ValueError, "duplicate paper"):
            builder.collect(self.root)

    def test_one_file_per_member_month(self):
        self.monthly()
        self.monthly("2026-10.yml")
        with self.assertRaisesRegex(ValueError, "one monthly YAML"):
            builder.collect(self.root)

    def test_monthly_invalid_shape_and_month(self):
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
                    builder.collect(self.root)
                self.assertEqual(json.loads((self.root / "data/added_at.json").read_text()), {})
            path.unlink()

    def test_invalid_ledger_is_not_silently_overwritten(self):
        (self.root / "data/added_at.json").write_text('{"bad": "2026-01-01"}')
        with self.assertRaisesRegex(ValueError, "timezone"):
            builder.collect(self.root)


if __name__ == "__main__":
    unittest.main()
