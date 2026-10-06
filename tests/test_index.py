import importlib.util
import json
from pathlib import Path
import re
import shutil
import sys
import unittest
from urllib.parse import unquote
import yaml
import test_build
ROOT = test_build.ROOT
sys.path.insert(0, str(ROOT / 'scripts'))
spec = importlib.util.spec_from_file_location('indexer', ROOT / 'scripts/index.py')
indexer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(indexer)


class IndexTests(unittest.TestCase):
    setUp = test_build.BuildTests.setUp
    monthly = test_build.BuildTests.monthly

    def test_global_dedup_across_months_and_members(self):
        self.monthly()
        config = json.loads((self.root / 'config/site.json').read_text())
        config['members']['reader-b'] = 'Reader B'
        (self.root / 'config/site.json').write_text(json.dumps(config))
        source = self.member_dir / '2026-10.yaml'
        other = self.root / 'entries/reader-b/2026-11.yaml'
        other.parent.mkdir(parents=True)
        other.write_text(source.read_text().replace("llm-inference", "quantization"))
        (self.root / 'data/added_at.json').write_text(json.dumps({
            'xzzWZY/arxiv:2309.06180': '2026-10-05T16:00:00Z',
            'reader-b/arxiv:2309.06180': '2026-11-02T16:00:00Z',
        }))
        shutil.copyfile(ROOT / 'CONTRIBUTING.md', self.root / 'CONTRIBUTING.md')
        shutil.copytree(ROOT / 'templates', self.root / 'templates')
        indexer.generate(self.root)
        home = (self.root / 'README.md').read_text()
        self.assertEqual(home.count('[PagedAttention]'), 1)
        self.assertIn('Reader B', home)
        catalog = self.root / 'catalog'
        self.assertFalse((catalog / 'by-month/2026-11.md').exists())
        self.assertFalse((catalog / 'by-week/2026-W45.md').exists())
        for member in ('xzzWZY', 'reader-b'):
            self.assertEqual((catalog / f'by-member/{member}.md').read_text().count('[PagedAttention]'), 1)
        self.assertEqual((catalog / 'by-topic/llm-inference.md').read_text().count('[PagedAttention]'), 1)
        self.assertEqual((catalog / 'by-topic/quantization.md').read_text().count('[PagedAttention]'), 1)
        for page in [self.root / 'README.md', *catalog.rglob('*.md')]:
            for target in re.findall(r'\]\(([^)]+)\)', page.read_text()):
                if not target.startswith(('http:', 'https:')):
                    self.assertTrue((page.parent / unquote(target)).exists(), (page, target))
        source.unlink()
        other.unlink()
        indexer.generate(self.root)
        self.assertNotIn('PagedAttention', (self.root / 'README.md').read_text())
        self.assertEqual(list((catalog / 'by-month').glob('20*.md')), [])
