# Organizer guide

Use one shared branch and one PR per week. Members keep their papers in monthly YAML files; the weekly branch is only the review batch.

## 1. Start the week

- Wait for the previous PR to merge and the **Update paper indexes** workflow to finish.
- Create `submissions/YYYY-Www` from the latest `main`, e.g. `submissions/2026-W41` (ISO week).
- Share the branch name and submission cutoff with the lab. Everyone commits to this branch and edits only their own `entries/First_Last/YYYY-MM.yaml`.
- Remind new members to register their name in `config/paperlist.json`. Topics are optional while collecting papers. Do not create a PR yet.

## 2. Collect submissions

Members sync the shared branch before editing. On GitHub, they select the weekly branch before editing their file and commit to that branch. Monthly files persist across weekly PRs; do not copy earlier papers into a new file. At a month boundary, members start the new monthly file even if the weekly branch stays the same.

## 3. Prepare the weekly PR

Announce a short editing pause, sync the branch, and ask your AI tool:

> Follow docs/classify-topics.md to prepare submissions/YYYY-Www. Fill missing topics using paper abstracts, run topic validation and tests, then commit, push, and open or update the single weekly PR to main. Include evidence and test results. Do not merge.

The AI uses the same weekly branch. It preserves existing tags and unrelated work. Review its proposed classifications and evidence. If a paper cannot be classified, supply the abstract or assign an appropriate existing topic yourself; do not use a placeholder tag.

Required checks:

```sh
.venv/bin/python scripts/validate.py --require-topics
.venv/bin/python -m unittest discover -s tests -q
```

Use an equivalent Python environment with `requirements.txt` installed if needed. Every paper must have one to three valid topics before opening the PR. GitHub's **Check paper submissions** workflow repeats validation on the PR. This workflow validates tags; it does not call AI or judge whether a tag is semantically correct.

## 4. Review and merge

- Confirm the PR targets `main` from the correct weekly branch, with no duplicate weekly PR.
- Review the submitted titles, URLs, venue/year, and AI topic evidence. Check that members did not accidentally change someone else's papers.
- Ensure all checks pass for the latest commit. If someone pushes after preparation, rerun classification/checks on the updated branch.
- Keep generated README/catalog files and `data/added_at.json` out of this weekly PR; the index bot owns them.
- Squash-merge the PR, then verify **Update paper indexes** succeeds and the new papers appear in the catalog.
- Delete the merged weekly branch. Start next week's branch from the updated `main`.

The month index uses the first successful ingestion after merge in America/Chicago, not the YAML filename. A September file merged for the first time in October is indexed under October.

## If something goes wrong

| Situation | Action |
| --- | --- |
| Missing topics | Run AI classification or manually classify; rerun checks before proceeding. |
| Unknown topic or malformed YAML | Use IDs from `config/paperlist.json` and fix the reported file. |
| Same member submitted a duplicate | Keep one entry and edit it; identical normalized titles from different members are allowed. |
| Push rejected or merge conflict | Sync and reconcile changes with the affected member, then rerun checks. Never force-push the shared branch. |
| Late contribution before merge | Add it to the same branch, classify it, and rerun checks. |
| Late contribution after merge | Use the next weekly branch, still editing the correct monthly file. |
| Index workflow fails | Inspect its Actions log, resolve the error, and rerun it before starting the next batch. |

## Repository settings

This is a team workflow convention. No branch protection has been configured by these changes. Passing checks do not technically prevent a merge unless the repository requires them. If branch protection is enabled later, account for the index bot: it currently writes generated indexes directly to `main` and would need a compatible update path.
