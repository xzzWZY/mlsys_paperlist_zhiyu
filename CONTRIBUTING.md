# Contribute

**One YAML file per member per month**, e.g. `entries/xzzWZY/2026-10.yaml`. Add or edit papers in the same file as often as you like during that month. Aim for about two papers per week.

## Format

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
    topics: [compilers-kernels, architectures]
```

`venue` and `code_url` are optional. Other fields are required. Choose 1–3 topic IDs from [config/site.json](config/site.json). Use spaces for indentation. No summaries or notes are needed.

## Submit or update

1. Open `entries/<your-username>/YYYY-MM.yaml` on GitHub. Create it using [the template](templates/monthly.yaml) if it does not exist; otherwise edit that file.
2. Append a new `- paper_id:` item for another paper, or edit an existing item to correct its metadata.
3. Commit to `main`, or merge a pull request. **Update paper indexes** updates the homepage and category pages automatically.

Your username must be registered in `config/site.json`. Next month, create a new file; do not copy previous papers into it. A monthly file may contain any positive number of papers. `.yaml` and `.yml` are supported, but use only one file per member per month.

## Deduplication

- **All papers:** one row per canonical paper ID, with all contributing members and their topics combined.
- **By month / week:** a paper appears only in its earliest recorded period across all members. Later submissions by other members do not repeat it in later time groups.
- **By topic:** one row per paper in each matching topic. A multi-topic paper is discoverable under each of its topics.
- **By member:** each member's submitted papers appear in their own list, with their own dates and topics.
- A member cannot submit the same paper twice, including across monthly files. Edit the existing entry instead.

arXiv IDs are case insensitive and version suffixes are ignored. DOI IDs are case insensitive. Use a consistent ID: the system does not automatically infer that an arXiv ID and a DOI refer to the same paper.

## Dates

The filename organizes your monthly submissions. Index dates come from the first successful ingestion in `America/Chicago`, not the filename or publication year. Adding a paper later timestamps only that new contribution; editing or moving an existing contribution keeps its date as long as its member and paper ID stay the same. Month/week indexes use the earliest contribution to each paper.

## Local validation

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/build.py --check
.venv/bin/python -m unittest discover -s tests -q
```

The homepage and `catalog/` are generated; edit YAML instead. The Actions bot needs permission to commit to `main`. If branch rules prevent that, include `python scripts/index.py --record` outputs in a reviewed PR. No Pages deployment is used.
