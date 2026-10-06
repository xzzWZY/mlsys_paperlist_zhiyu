# Contribute

1. Select the current automatically created weekly branch on GitHub, e.g. `submissions/2026-10-05_to_2026-10-12`. Ask the organizer which branch is active if unsure. **Push all contributions to this shared branch, not `main`; do not create your own branch or PR.** Sync the branch before editing.
2. Create or update your monthly file, e.g. `entries/Zhiyu_Wu/2026-10.yaml`. Keep using it across weeks and only edit your own entries.

```yaml
papers:
  - title: "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness"
    url: "https://arxiv.org/abs/2205.14135"
    year: 2022
    venue: "NeurIPS"
```

**Required:** `title`, `url` (HTTP/HTTPS), `year`. **Optional:** `venue`. Copy the [template](templates/monthly.yaml) to add more papers. Register your full name with underscores in [config/paperlist.json](config/paperlist.json) the first time.

Members do not need to provide topics. The organizer calls AI to classify papers, runs checks, and merges one shared PR each week. The next submission branch is then created automatically when the feature is enabled. If no branch exists, contact the organizer.

Copy the full paper title: title matching ignores case, all whitespace, punctuation, and invisible formatting characters (including full-width variants). Matching titles are deduplicated across members; meaningful symbols such as `+` remain distinct. Edit your existing entry instead of submitting it again. Do not edit generated indexes.
