# UIUC-MLSys paperlist

[All papers](catalog/README.md) · [By week](catalog/by-week/README.md) · [By topic](catalog/by-topic/README.md) · [By member](catalog/by-member/README.md)

[Contribute](CONTRIBUTING.md) · [Weekly YAML template](templates/weekly.yaml) · [Examples](catalog/examples/README.md)

One YAML file per member per week. GitHub Actions updates the linked Markdown tables after submissions reach `main`. No GitHub Pages or external hosting is required.

## Example library

[Browse 5 example papers](catalog/examples/README.md) across 3 weeks and 2 fictional members. PagedAttention is submitted by both members to demonstrate deduplication. All dates and member assignments are illustrative.

## Search

Browse the indexes above, click topic/member/week links inside a table, or use your browser's Find on a rendered page. These are static GitHub tables, not interactive website filters.

For repository code search, use **Search this repository** and add a title, paper ID, topic ID, or member. Restrict searches to source submissions to avoid matching generated copies:

```text
repo:xzzWZY/mlsys_paperlist_zhiyu path:entries/ "llm-inference"
repo:xzzWZY/mlsys_paperlist_zhiyu path:entries/xzzWZY/ "FlashAttention"
repo:xzzWZY/mlsys_paperlist_zhiyu path:2026-W41.yaml
```

For a weekly filename anywhere under a member folder, use `path:2026-W41.yaml`. The filename reflects the submission batch; the **By week** index reflects first recorded arrival time. Replace the repository qualifier when moving to the lab repo. Search indexing can lag; the Markdown indexes are the primary browsing interface.

## Maintainer setup

1. Use a **private repository** for lab papers and grant access to lab members. This code change does not change the visibility of the existing personal prototype.
2. Update `config/site.json` with the repository URL, title, member usernames, and topics.
3. Enable Actions. **Update paper indexes** needs `contents: write` and permission to commit to `main`. If branch rules prevent bot writes, generate indexes locally with `--record` and include them in a reviewed PR instead; do not weaken lab branch protections.
4. If this repository previously published a Pages site, **unpublish it in Settings → Pages**. Removing the deployment workflow alone does not remove an already published site. Do this before adding private lab content.

The bot records timestamps and commits `catalog/` plus `data/added_at.json`. A failed validation leaves existing indexes intact. Concurrent pushes cause regeneration against the latest `main`, rather than overwriting newer submissions. PRs only validate; merged submissions update the indexes.

## Local checks

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/build.py --check
.venv/bin/python scripts/index.py
```

Use `scripts/index.py --record` when intentionally recording new submissions. Without it, dates for unrecorded entries are provisional. The previous website source remains in `site/` for reference, but no workflow builds or deploys it.
