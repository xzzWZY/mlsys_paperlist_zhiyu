# Add your weekly papers

**One member, one YAML file per week.** Aim for two papers; add more or fewer as needed. All paper information should be in English.

## Complete example

For October 5–11, 2026 (ISO week 41), create:

```text
entries/xzzWZY/2026-W41.yaml
```

Paste this content. Unlike the old Markdown format, no `---` delimiters or written notes are needed:

```yaml
papers:
  - paper_id: "arxiv:2309.06180"
    title: "Efficient Memory Management for Large Language Model Serving with PagedAttention"
    url: "https://arxiv.org/abs/2309.06180"
    year: 2023
    venue: "arXiv"
    topics: [llm-inference, hardware-systems]

  - paper_id: "arxiv:2205.14135"
    title: "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness"
    url: "https://arxiv.org/abs/2205.14135"
    year: 2022
    venue: "arXiv"
    topics: [compilers-kernels, architectures]
```

`papers:` starts the list. Each `- paper_id:` starts a new paper. Keep the indentation shown above and use spaces, not tabs. Replace the examples with papers you want to share.

| Field | Meaning |
| --- | --- |
| `paper_id` | Required: `arxiv:<ID>` or `doi:<ID>`. Use the same ID when different members submit the same paper. |
| `title` | Required: full title in quotes. |
| `url` | Required: HTTP(S) paper link. |
| `year` | Required: publication year as a number. |
| `topics` | Required: 1–3 exact IDs from [config/site.json](config/site.json). |
| `venue` | Optional: conference, journal, or `Preprint`. |
| `code_url` | Optional: HTTP(S) code link. |

## Submit in your browser

1. Open the [repository](https://github.com/xzzWZY/mlsys_paperlist_zhiyu) on `main`.
2. Select **Add file → Create new file**. Enter `entries/<your-username>/YYYY-Www.yaml`, replacing the username and ISO year/week. Your username must be registered in [config/site.json](config/site.json); `xzzWZY` is registered already.
3. Paste the example or [weekly template](templates/weekly.yaml), then fill in your papers.
4. Click **Commit changes…** and commit to `main`, or open a pull request and merge it after checks pass.
5. Wait for **Actions → Publish paperlist** to succeed, then refresh the [website](https://xzzWZY.github.io/mlsys_paperlist_zhiyu/). Turn off **Example library** and reset filters to see real contributions.

Already submitted this week? Edit that same YAML file and append another paper to `papers:`. Next week, create a new file, e.g. `2026-W42.yaml`. Do not copy last week's papers into the new file.

## Submit locally

From your repository directory:

```sh
git pull --rebase origin main
cp templates/weekly.yaml entries/xzzWZY/2026-W41.yaml
# Edit the new file. If it already exists, edit it without copying over it.
git add entries/xzzWZY/2026-W41.yaml
git commit -m "Add papers for week 41"
git push origin main
```

Change the filename to the appropriate ISO week. With [Python setup](README.md#local-preview) complete, optionally validate before committing:

```sh
.venv/bin/python scripts/build.py --check
```

## Dates, grouping, and duplicates

- The filename organizes your weekly submission; it does not override the website's submission timestamp. A late upload appears in the week it is first recorded by the publishing workflow, even if its filename names an earlier week.
- Weeks run Monday–Sunday in `America/Chicago`. The first successful ingestion time approximates arrival on `main`; it is not an exact push-event timestamp.
- Each paper has its own persistent timestamp. Appending a paper later gives only that new paper a new timestamp. Editing or migrating an existing paper keeps its date when the member and paper ID stay the same.
- One member may submit a paper once across all weekly files. arXiv versions count as one paper. Different members may submit the same paper, and the table groups their contributions within the selected week/topic/member group.
- One weekly file per member is allowed (`.yaml` preferred; `.yml` also accepted). Filenames must use a real ISO week, including two digits, such as `2026-W05.yaml`.
- Paper totals count unique papers. Member statistics count submissions; the four-week average includes the current partial week and the three preceding weeks. Two per week is a guideline, not a validation requirement.
- Existing single-paper Markdown files remain readable for compatibility. To migrate, move their metadata into a weekly YAML file and remove the old Markdown file in the same commit. Do not retain both copies. No new Markdown files are needed.

## Reading the table

Switch **By week / By topic / By member**, combine search and filters, and use **Sort papers** for newest/oldest added, title, or publication year. Sorting applies within each group. Click a title to read the paper; click a contributor to open the source submission. On narrow screens, scroll the table horizontally.

## Common errors

| Error | Fix |
| --- | --- |
| Unknown member | Match the username registered in `config/site.json`, including case. |
| Invalid topic | Use exact topic IDs, e.g. `llm-inference`, not display labels. |
| Invalid YAML | Check indentation and quotes. `papers:` must contain a nonempty list. |
| Invalid week | Use `YYYY-Www.yaml` with a real ISO week number. |
| Duplicate paper | Remove the duplicate from this or another weekly file; edit the original entry. |
| Paper not visible | Check `main`, a successful publish run, example mode, and filters. |

See [deployment setup](README.md#enable-public-github-pages) for the maintainer's one-time configuration.
