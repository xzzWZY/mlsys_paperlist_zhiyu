# Contribute

1. Use the lab's shared weekly branch, e.g. `submissions/2026-W41`. The organizer creates it from the latest `main`. Sync it before editing; on GitHub, select it in the branch menu.
2. Edit your monthly file, e.g. `entries/Zhiyu_Wu/2026-10.yaml`, and commit to the shared branch. Keep using this monthly file across weeks; only edit your own entries.

```yaml
papers:
  - title: "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness"
    url: "https://arxiv.org/abs/2205.14135"
    year: 2022
    venue: "NeurIPS"
```

**Required:** `title`, `url` (HTTP/HTTPS), `year`. **Optional:** `venue`, `code_url`. Members do not need to add topics; AI classification is required before the weekly PR. Copy the [template](templates/monthly.yaml) for more papers. Register your full name with underscores in [config/paperlist.json](config/paperlist.json) the first time.

## Weekly PR

Organizer: follow the [weekly checklist](docs/organizer.md).

The organizer coordinates a brief editing pause, then asks an AI tool:

> Follow docs/classify-topics.md to prepare this week's shared branch: classify missing topics, run the required checks, then commit, push, and open or update the weekly PR to main. Include classification evidence and test results.

Each week has one shared PR. After checks pass, the organizer reviews and squash-merges it. Indexes update automatically. Delete the merged branch and create next week's branch from the updated `main`. No individual or separate classification PRs are needed.

Papers without topics may stay on the working branch, but fail the PR check. If AI cannot classify a paper, the organizer must resolve it before opening/merging the PR. Do not edit generated indexes. Duplicate titles are merged across members; edit your existing entry instead of resubmitting it.
