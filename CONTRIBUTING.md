# Add a paper

Aim for **two papers per week**. Each paper needs one Markdown file with basic information only. Write titles and metadata in English.

## A complete example

Create `entries/xzzWZY/pagedattention.md` with this content:

```markdown
---
paper_id: "arxiv:2309.06180"
title: "Efficient Memory Management for Large Language Model Serving with PagedAttention"
url: "https://arxiv.org/abs/2309.06180"
year: 2023
venue: "arXiv"
topics:
  - llm-inference
  - hardware-systems
---
```

Copy the contents of the block, without the surrounding triple backticks. For another paper, change the filename and metadata. Use your own registered GitHub username in place of `xzzWZY`.

| Field | What to enter |
| --- | --- |
| `paper_id` | The arXiv identifier prefixed with `arxiv:`, or a DOI prefixed with `doi:`. |
| `title` | Full paper title in quotes. |
| `url` | HTTP(S) link to the paper. |
| `year` | Publication year as a number, not the submission year. |
| `topics` | 1–3 exact IDs from [config/site.json](config/site.json), such as `llm-inference` or `compilers-kernels`. |
| `venue` | Optional conference, journal, or `Preprint`. |
| `code_url` | Optional HTTP(S) link to the code. |

Keep both `---` lines. Use spaces before topic list items, not tabs. No text is needed below the closing `---`.

## Submit in your browser

1. Open the [repository](https://github.com/xzzWZY/mlsys_paperlist_zhiyu) on the `main` branch.
2. Select **Add file → Create new file**.
3. Enter `entries/<your-username>/<paper-name>.md` as the filename and paste your completed metadata.
4. Click **Commit changes…**, with a message such as `Add PagedAttention`. Commit to `main` if permitted, or open a pull request and have it merged.
5. Wait for **Actions → Publish paperlist** to finish successfully.
6. Refresh the [website](https://xzzWZY.github.io/mlsys_paperlist_zhiyu/). Uncheck **Example library** to see real submissions; use **Reset filters** if needed.

Your username must first be registered under `members` in [config/site.json](config/site.json). `xzzWZY` is already registered. Ask the maintainer to add other members and provide repository access.

## Submit with Git

In your local repository, get the latest changes and copy the [template](templates/paper.md) to a new filename:

```sh
git pull --rebase origin main
cp templates/paper.md entries/xzzWZY/my-paper.md
```

Edit the new file, replace the template values, then commit and push:

```sh
git add entries/xzzWZY/my-paper.md
git commit -m "Add paper"
git push origin main
```

GitHub Actions checks the format automatically. For optional local validation, follow the [Python setup](README.md#local-preview), then run `.venv/bin/python scripts/build.py --check`.

## What happens automatically?

- The website displays the title, paper link, topics, and contributor. Paper details also show the publication metadata and contribution dates.
- The member folder identifies the contributor. Do not add member, date, or week fields.
- The first successful publishing workflow records the entry's time. This approximates arrival on `main`, rather than the exact push time. Weeks run Monday–Sunday in `America/Chicago`.
- Edits and filename changes keep the original week when the member and paper ID remain the same. Keep IDs stable; ask the maintainer to migrate a timestamp if an ID needs correction.
- Each member can submit a paper once. Different members can submit the same paper; the website groups their contributions under its canonical ID. arXiv versions count as one paper. Use the same identifier across members: DOI and arXiv IDs are not automatically cross-matched.
- Paper totals count unique papers; member totals count submissions. The weekly average covers the current partial week and the previous three weeks, divided by four. The two-paper target is a guideline, not a validation requirement.
- Examples are separate from real contributions and never count toward member totals.

## If something goes wrong

| Problem | Fix |
| --- | --- |
| Unknown member | Match the registered username, including capitalization. |
| Invalid topic | Copy an exact ID from the configuration, not a display label. |
| Invalid metadata | Keep the `---` lines, quote text values, and enter the year as a number. |
| Duplicate paper | Edit your existing file instead of creating a second submission. |
| Paper not visible | Check that it is on `main`, the publish workflow succeeded, examples are off, and filters are reset. |
| Website displays the README | Select **Settings → Pages → Source → GitHub Actions**, then run **Publish paperlist**. |

See the [deployment instructions](README.md#enable-public-github-pages) for the maintainer's one-time setup.
