# Weekly PR guide — organizers only

Members push to one shared dated branch and maintain monthly YAML files. You classify and merge one PR each week; members do not create individual PRs.

## Setup and switch

**Start next submission period** (`.github/workflows/next-submission.yml`) runs only after a same-repository submission PR is merged into `main`. Closing without merging, ordinary pushes, and unrelated PRs do not create a branch. There is no schedule or manual-dispatch trigger.

In **Settings → Secrets and variables → Actions → Variables**, set the repository variable `AUTO_CREATE_SUBMISSION_BRANCH`:

| Value | Behavior |
| --- | --- |
| `true` or unset | Automatically create the next dated branch after an eligible merge. |
| `false` | Disable creation; existing branches remain untouched. |

The workflow needs Actions enabled and `contents: write` permission (declared in the workflow). No model API key is needed. It creates a branch, not a PR, and never runs AI.

For the first batch, create one branch manually from the latest `main`, using the naming rule below. There is no earlier merged PR to bootstrap it. When automation is disabled, create subsequent branches manually as needed. Enabling the variable alone does not trigger a run.

## Date naming

- Branch: `submissions/2026-10-05_to_2026-10-12`.
- PR title: `Paper submission [2026-10-05 ~ 2026-10-12]`.
- Start: previous PR's merge date in **America/Chicago**. End: the strictly following Monday. A Monday merge starts a seven-day period.
- The branch uses `_to_` because spaces, brackets, and `~` cannot be used as shown in a Git branch name.
- Merge time fixes the date range: retrying a run on another day creates the same name. Existing branches are left unchanged, never reset. Multiple merges on one local date reuse the same dated branch.

## 1. Collect papers

After the previous merge, check **Actions → Start next submission period**. It updates indexes on main, then creates the dated branch from the latest main. It shares a concurrency group with the index workflow to serialize their writes. The run summary records the resulting branch.

Share the active branch and cutoff with the lab. Members sync before editing, push only to this branch, and modify their own `entries/First_Last/YYYY-MM.yaml`. At month boundaries they create the new monthly file, even if the weekly branch remains the same. Missing topics are allowed during collection.

## 2. Classify and open the weekly PR

Coordinate a brief editing pause and sync the shared branch. Ask your AI tool:

> Follow docs/classify-topics.md to prepare submissions/START_to_END (replace with the active branch). Fill missing topics using abstracts, run required validation and tests, then commit, push, and open or update the single PR to main. Include evidence and results. Do not merge.

AI works on the same branch. Review its evidence and classifications; resolve missing topics manually if necessary. Never use placeholder tags just to pass checks.

```sh
.venv/bin/python scripts/validate.py --require-topics
.venv/bin/python -m unittest discover -s tests -q
```

Use a Python environment with `requirements.txt` installed. All papers need one to three valid topics before opening the PR. The PR workflow repeats these checks; it does not call AI or assess the meaning of a topic.

## 3. Review and merge once per week

- Confirm the dated branch, `main` target, and absence of duplicate PRs.
- Review titles, links, year/venue, and topic evidence. Keep generated indexes and `data/added_at.json` out of submission PRs.
- Require green checks on the latest commit. If members push more papers, rerun classification/checks before merging.
- Squash-merge. Verify the catalog update and next-branch workflow succeed. Delete the old merged branch if desired; automation does not delete it.
- Share the newly created branch. Do not manually create another while the workflow is running.

The month index uses first ingestion after merge in America/Chicago, not the monthly filename. A September entry first merged in October is indexed under October.

## Recovery and limits

| Situation | Action |
| --- | --- |
| Missing/invalid topic or YAML | Fix the reported entry, then rerun required checks. |
| Duplicate paper by one member | Keep one entry; edit it instead. Different members may submit the same title. |
| Concurrent push or conflict | Reconcile with the member, sync, and rerun checks. Never force-push. |
| Late paper after merge | Use the new shared branch and the appropriate monthly file. |
| Workflow failure | Fix the Actions error and rerun the original merged-PR run. An existing destination branch will not be overwritten. |
| Wrong or stale existing branch | Inspect its commits with contributors; automation deliberately leaves it unchanged. Do not delete or reset member work. |
| Automation disabled | The organizer creates the next dated branch manually from updated main. |

No branch protection is configured by this setup. Checks are advisory until required by repository settings. The index bot currently pushes generated files to main; future protection rules must accommodate or replace that update path. README's “organizers only” label identifies the intended audience, not an access restriction.
