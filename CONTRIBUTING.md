# Add a paper

Aim for **two research-relevant papers per week**. A useful short note is more valuable than a pasted abstract. Write in English.

## What am I contributing?

**One paper = one Markdown file containing the paper's information and your reading note.** You do not need to edit HTML, upload a PDF, or update a spreadsheet. Markdown is a plain-text format; a line beginning with `##` is a section heading.

For example, if `xzzWZY` reads PagedAttention, the new file belongs here:

```text
entries/xzzWZY/pagedattention.md
        └─ member  └─ a short filename ending in .md
```

For a second paper, create a second file such as `entries/xzzWZY/flashattention.md`. Do not put two papers into the same file. Another member uses their own folder.

Before your first contribution, make sure your GitHub username is listed under `members` in [config/site.json](config/site.json). `xzzWZY` is already registered. Ask the repository maintainer to register other members and grant contribution access.

## Option A — Add a paper in your browser (easiest)

No terminal or Python installation is needed.

1. Open the [repository's Code page](https://github.com/xzzWZY/mlsys_paperlist_zhiyu) and select the `main` branch.
2. Choose **Add file → Create new file**.
3. In the filename box, enter `entries/xzzWZY/pagedattention.md`. Use your own registered username if you are a different member. If this file already exists, edit it rather than creating another copy of the same paper.
4. Paste the complete example below into the editor. Keep both `---` lines and the section headings. For your real contribution, replace the paper information and write your own summary and research connection.
5. Click **Commit changes…**. Enter a short message, such as `Add PagedAttention reading note`.
6. If you have permission to commit directly to `main`, select that option and confirm. Otherwise, choose a new branch, open a pull request, and wait for it to be merged into `main` after checks pass.
7. Open the repository's **Actions** tab. Find **Publish paperlist** for your change, and wait until both `build` and `deploy` succeed. A pull request that has not been merged only runs checks; it does not update the website.
8. Refresh the [paperlist website](https://xzzWZY.github.io/mlsys_paperlist_zhiyu/). Make sure **Example library is unchecked** to see real submissions. If old filters are hiding your paper, click **Reset filters**.

The site must have GitHub Pages enabled once by the maintainer. See [deployment setup](README.md#enable-public-github-pages) if it has not been configured yet.

## Complete example — PagedAttention

Copy only the contents of this code block into the `.md` file, not the surrounding triple backticks. This is an illustrative note based on the paper's abstract; replace the research connection with your own reasoning before submitting it as your contribution.

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

## Summary
PagedAttention manages the key-value cache in blocks, using ideas from
virtual memory. The vLLM system uses this design to reduce fragmentation
and share cache memory, allowing more requests to be batched together.

## Relevance to my research
I am interested in inference scheduling under variable request lengths.
This paper suggests that memory allocation and scheduling should be
studied together, because cache utilization affects feasible batch sizes.

## Limitations / Questions
How would the tradeoffs change for workloads dominated by short requests?
```

### How to fill it in

- **`paper_id`** is the paper's stable identifier. For `https://arxiv.org/abs/2309.06180`, use `arxiv:2309.06180`. It is not your username or an arbitrary nickname.
- **`title`** is the full paper title. Keep quotation marks around it, especially when the title contains a colon.
- **`url`** is the link readers should open to read the paper.
- **`year`** is the paper's publication year, not the year you added it to the list.
- **`venue`** is optional. You can write `Preprint` if appropriate or remove this line.
- **`topics`** determines which topic pages show the paper. Use 1–3 exact IDs from the list below, with two spaces before each `-`.
- **Summary:** what problem does the paper address, what is the main idea, and what does it show? Aim for 2–4 sentences in your own words.
- **Relevance to my research:** why did you select this paper? Name a connection to your project, a method you might try, or an experiment it inspires. Aim for 1–3 sentences.
- **Limitations / Questions:** optional. Add a concern or discussion question, or remove this entire section.

You do **not** add `author`, `member`, `date`, `week`, or `added_at` fields. Your member folder identifies the contributor, and the publishing workflow records the submission time.

### What will appear on the website?

After the note is accepted and deployed:

- **By week:** the note appears under its first recorded contribution week, not the paper's publication year.
- **By topic:** this example appears under both **LLM inference** and **Hardware & systems**.
- **By member:** it appears under **Zhiyu Wu**, the display name registered for `xzzWZY`, and adds one contribution.
- **Paper details:** clicking the paper title opens your full summary, research connection, and questions.
- **Library totals:** the paper counts once even though it has two topics. If another member already submitted it using the same `paper_id`, your note joins the existing paper's details.

## Option B — Add a paper using Git locally

If you already have the repository on your computer, open a terminal in that directory. Start by getting the latest changes, then copy the template:

```sh
git pull --rebase origin main
cp templates/paper.md entries/xzzWZY/pagedattention.md
```

Open the new file in your editor and fill it in using the example above. Choose a different filename for a different paper; do not overwrite an existing note accidentally.

If you want to check your file locally, set up Python once:

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Then validate and submit:

```sh
.venv/bin/python scripts/build.py --check
git add entries/xzzWZY/pagedattention.md
git commit -m "Add PagedAttention reading note"
git push origin main
```

Local validation is optional; GitHub Actions also validates submissions. If validation fails, fix the reported file and field before pushing. If Git rejects the push because the remote has newer commits, pull with `git pull --rebase origin main`, resolve any conflicts, and push again.

## Available topics

Copy the ID on the left into your file. The configuration file is the authoritative list if this table changes later.

| Topic ID | Website label |
| --- | --- |
| `llm-inference` | LLM inference |
| `distributed-training` | Distributed training |
| `compilers-kernels` | Compilers & kernels |
| `hardware-systems` | Hardware & systems |
| `quantization` | Quantization |
| `pruning-distillation` | Pruning & distillation |
| `efficient-finetuning` | Efficient fine-tuning |
| `optimization` | Optimization |
| `architectures` | Architectures |
| `reasoning-agents` | Reasoning & agents |
| `rl-post-training` | RL & post-training |
| `data-centric-ml` | Data-centric ML |
| `evaluation` | Evaluation |
| `multimodal` | Multimodal learning |

## Common problems

| What happened? | What to do |
| --- | --- |
| `unknown member` | Make the folder name match a username registered in `config/site.json`, including capitalization. |
| Invalid topic | Use an exact topic ID such as `llm-inference`, not the display label `LLM inference`. |
| Missing Summary or research relevance | Keep the exact required headings and write content under both. Do not leave the template's `Replace with` text. |
| YAML/front matter error | Keep the opening and closing `---`, quote text values, and use spaces rather than tabs for topic indentation. |
| Duplicate paper for this member | Edit your existing note. A new arXiv version does not count as a different paper. |
| My note is in GitHub but missing from the website | Confirm it is on `main`, check **Publish paperlist** for a successful deployment, refresh, uncheck **Example library**, and reset filters. |
| I still see only the two example papers | Uncheck **Example library**. Real notes belong in `entries/`, not `examples/`. |
| The site shows a README instead of paper cards | Set **Settings → Pages → Source** to **GitHub Actions**, then run **Publish paperlist**. |

To fix a submitted note, edit the same file, commit, and push again. You do not need to delete and resubmit it.

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
