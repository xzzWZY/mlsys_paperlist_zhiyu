# Add a paper

Aim for **two research-relevant papers per week**. A useful short note is more valuable than a pasted abstract. Write in English.

## Three steps

1. Copy `templates/paper.md` to `entries/<your-github-username>/<short-paper-name>.md`. Your username must appear in `config/site.json`.
2. Fill in the metadata, **Summary**, and **Relevance to my research**. Add optional questions and a `code_url` if useful. Choose 1–3 topic IDs from `config/site.json`.
3. Commit and push to `main`, or open a pull request and merge it after the checks pass. The publishing workflow updates the website automatically once Pages is enabled.

For this personal prototype:

```sh
cp templates/paper.md entries/xzzWZY/my-paper.md
# Edit the new file before running validation.
.venv/bin/python scripts/build.py --check
git add entries/xzzWZY/my-paper.md
git commit -m "Add reading note on my paper"
git push origin main
```

You can also create the file in GitHub's web editor. No local Python installation is required for web submissions; GitHub Actions validates them.

## Metadata rules

| Field | Rule |
| --- | --- |
| `paper_id` | Stable `arxiv:2309.06180` or `doi:10.xxxx/...` identifier. arXiv versions are merged; DOI IDs are case insensitive. |
| `title` | Full paper title. |
| `url` | Absolute HTTP(S) link to the paper. |
| `year` | Four-digit publication year, without quotes. |
| `topics` | 1–3 distinct IDs from `config/site.json`. |
| `venue` | Optional conference, journal, or `Preprint`. |
| `code_url` | Optional absolute HTTP(S) code link. |

Choose one canonical identifier for a paper across members. The system does not automatically recognize that a DOI and an arXiv ID describe the same paper. Request a new topic by editing `config/site.json`.

## Time and counting

- Weeks use ISO week numbers, Monday–Sunday, in `America/Chicago`.
- `added_at` is the first successful publishing-workflow ingestion time, stored in `data/added_at.json`. It approximates the time a contribution reaches `main`; it is **not the local commit date or the exact push event time**. A failed or delayed run can shift an unrecorded submission into a later week.
- Do not fill in or modify dates in a paper file. Local previews use a clearly labeled provisional timestamp until publication records it.
- Editing or renaming a note preserves its original week, as long as the member and canonical paper ID stay the same. Deleting and re-adding the same paper also retains its first timestamp.
- One member may submit one note per paper. Multiple members may contribute different notes about the same paper; the paper details show all of them.
- Paper totals count unique canonical IDs. Contribution totals count individual notes. A multi-topic paper can appear under several topic groups without inflating the library total.
- The four-week average includes the current partial week and the preceding three ISO weeks, divided by four. Member statistics describe the whole selected library, even when note filters are active. Missing the target does not fail a build.
- Example notes live in `examples/`, are labeled, and never count toward real member contributions. Their fixed dates are for demonstration only. The example switch selects the example library instead of the real library.

## Markdown

Use paragraphs, headings, lists, emphasis, fenced code, and links. Raw HTML is displayed as text, and unsafe links are stripped. Required sections must use exactly `## Summary` and `## Relevance to my research`.

Keep IDs stable. Changing an ID or moving a note to a different member creates a new contribution identity. For intentional identity corrections, migrate the matching ledger key rather than inventing a new date.
