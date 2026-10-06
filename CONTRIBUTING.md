# Contribute

1. Create or edit `entries/First_Last/YYYY-MM.yaml`, e.g. `entries/Zhiyu_Wu/2026-10.yaml`. Use one file per month and update it whenever you add papers.
2. Copy the [template](templates/monthly.yaml), or append another item:

```yaml
papers:
  - title: "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness"
    url: "https://arxiv.org/abs/2205.14135"
    year: 2022
    venue: "NeurIPS"
```

3. Commit to `main` or merge a pull request. Paper indexes update automatically.

**Required:** `title`, `url` (HTTP/HTTPS), `year`. **Optional:** `venue`, `code_url`. No summary or topics are needed; untagged papers appear under **Uncategorized** until classified. Optional `topics` may contain up to three IDs from [the topic list](config/paperlist.json).

Use your full name with underscores; add it to `members` in [config/paperlist.json](config/paperlist.json) when contributing for the first time. Copy the paper's full title: deduplication ignores case, spacing, and punctuation separators. Edit your existing entry instead of submitting it again. Changing the title wording creates a new identity and first-added date.
