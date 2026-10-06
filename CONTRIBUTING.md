# Contribute

1. Create a branch from the latest `main`, e.g. `papers/Zhiyu_Wu/2026-10`. Create or edit `entries/First_Last/YYYY-MM.yaml`, e.g. `entries/Zhiyu_Wu/2026-10.yaml`. Use one file per month and update it whenever you add papers.
2. Copy the [template](templates/monthly.yaml), or append another item:

```yaml
papers:
  - title: "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness"
    url: "https://arxiv.org/abs/2205.14135"
    year: 2022
    venue: "NeurIPS"
```

3. Commit to your branch and open a pull request to `main`. While it is open, keep adding to the same branch and PR. Ask the meeting organizer to review and merge after checks pass. After a merge, start a fresh branch from the latest `main` for further updates, editing the same monthly YAML. Paper indexes update automatically after merge.

On GitHub, choose **Create a new branch for this commit and start a pull request** when saving your first edit. Submit the YAML changes (and member registration if needed); do not edit generated indexes.

**Required:** `title`, `url` (HTTP/HTTPS), `year`. **Optional:** `venue`, `code_url`. No summary or topics are needed; untagged papers appear under **Uncategorized** until classified. Optional `topics` may contain up to three IDs from [the topic list](config/paperlist.json).

Use your full name with underscores; add it to `members` in [config/paperlist.json](config/paperlist.json) when contributing for the first time. Copy the paper's full title: deduplication ignores case, spacing, and punctuation separators. Edit your existing entry instead of submitting it again. Changing the title wording creates a new identity and first-added date.

## Add topics with AI

Any member or meeting organizer can ask their AI tool:

> Follow docs/classify-topics.md to classify untagged papers. Show the proposed topics, evidence, and validation results for review.

Review the changes and submit a separate classification PR. Existing tags stay unchanged unless you request corrections. Papers that cannot be classified remain under **Uncategorized**.
