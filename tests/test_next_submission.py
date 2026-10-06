import sys
from pathlib import Path
import unittest
from unittest.mock import Mock
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from next_submission import next_branch, create_branch


def event(merged_at='2026-10-05T18:00:00Z'):
    return {'action': 'closed', 'pull_request': {'merged': True, 'merged_at': merged_at,
            'base': {'ref': 'main'}, 'head': {'ref': 'submissions/2026-09-28_to_2026-10-05',
                                          'repo': {'full_name': 'lab/papers'}}}}


class NextSubmissionTests(unittest.TestCase):
    def test_monday_moves_to_following_monday(self):
        self.assertEqual(next_branch(event(), 'lab/papers'), 'submissions/2026-10-05_to_2026-10-12')

    def test_timezone_sunday_and_year_boundary(self):
        self.assertEqual(next_branch(event('2026-10-05T02:00:00Z'), 'lab/papers'), 'submissions/2026-10-04_to_2026-10-05')
        self.assertEqual(next_branch(event('2026-12-31T18:00:00Z'), 'lab/papers'), 'submissions/2026-12-31_to_2027-01-04')

    def test_only_enabled_merged_submission_prs(self):
        self.assertIsNone(next_branch(event(), 'lab/papers', False))
        self.assertIsNone(next_branch(event(), 'other/repo'))
        for field, value in [('merged', False), ('base', {'ref': 'dev'}), ('head', {'ref': 'feature/docs'})]:
            e = event(); e['pull_request'][field] = value
            self.assertIsNone(next_branch(e, 'lab/papers'))
        e = event(); e['action'] = 'opened'
        self.assertIsNone(next_branch(e, 'lab/papers'))
        self.assertIsNone(next_branch({}, 'lab/papers'))

    def test_existing_branch_never_reset(self):
        api = Mock(return_value={'object': {'sha': 'member-work'}})
        self.assertIn('unchanged', create_branch(api, 'lab/papers', 'submissions/test'))
        self.assertEqual(api.call_count, 1)

    def test_create_from_latest_main(self):
        api = Mock(side_effect=[None, {'object': {'sha': 'latest-index-commit'}}, {}])
        create_branch(api, 'lab/papers', 'submissions/test')
        self.assertEqual(api.call_args.args, ('POST', '/repos/lab/papers/git/refs',
                                            {'ref': 'refs/heads/submissions/test', 'sha': 'latest-index-commit'}))
