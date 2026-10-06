import importlib.util
from pathlib import Path
import re
import sys
from urllib.parse import unquote

import unittest
import test_build
ROOT = test_build.ROOT

sys.path.insert(0, str(ROOT / 'scripts'))
spec = importlib.util.spec_from_file_location('indexer', ROOT / 'scripts/index.py')
indexer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(indexer)


class IndexTests(unittest.TestCase):
    setUp = test_build.BuildTests.setUp
    weekly = test_build.BuildTests.weekly
    def test_index_links_and_separate_examples(self):
        import shutil
        shutil.copytree(ROOT / 'examples', self.root / 'examples')
        shutil.copyfile(ROOT / 'CONTRIBUTING.md', self.root / 'CONTRIBUTING.md')
        self.weekly()
        indexer.generate(self.root, record=True)
        catalog = self.root / 'catalog'
        self.assertNotIn('FlashAttention', (catalog / 'README.md').read_text())
        self.assertIn('FlashAttention', (catalog / 'examples/README.md').read_text())
        for page in catalog.rglob('*.md'):
            for target in re.findall(r'\]\(([^)]+)\)', page.read_text()):
                if not target.startswith(('http:', 'https:')):
                    self.assertTrue((page.parent / unquote(target)).exists(), (page, target))
        member = catalog / 'by-member/xzzWZY.md'
        self.assertIn('PagedAttention', member.read_text())
        (self.member_dir / '2026-W41.yaml').unlink()
        indexer.generate(self.root)
        self.assertNotIn('PagedAttention', member.read_text())
        self.assertEqual(list((catalog / 'by-week').glob('20*.md')), [])
