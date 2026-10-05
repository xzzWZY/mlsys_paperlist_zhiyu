# Zhiyu's paperlist

A public prototype of a shared reading library for **ML systems and ML algorithms**. Add a Markdown note, push it, and let GitHub Actions validate and publish the library.

Features: weekly / topic / member views, full-note search, combined filters, paper details with multiple contributors, stable first-seen dates, and a rolling four-week contribution average. All content and controls are in English. No database, frontend build tool, or external font service is required.

## Start reading or contributing

- [Contribution guide](CONTRIBUTING.md)
- [Copy the paper template](templates/paper.md)
- [Configure members, topics, and site identity](config/site.json)
- Intended public URL **after deployment is enabled**: https://xzzWZY.github.io/mlsys_paperlist_zhiyu/

Two clearly labeled example notes demonstrate the interface. They summarize [PagedAttention](https://arxiv.org/abs/2309.06180) and [FlashAttention](https://arxiv.org/abs/2205.14135), based on their abstracts, with illustrative discussion prompts. They are not the owner's reading history. The site starts in example mode only when no real notes exist.

## Local preview

Requires Python 3.9 or newer:

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/build.py
.venv/bin/python -m http.server 8000 --bind 127.0.0.1 --directory dist
```

Open http://localhost:8000. Generated files live in ignored `dist/`. Relative assets support both the local preview and GitHub Pages project subpaths. Do not use `--record` for ordinary previews: only publication should persist first-seen timestamps.

## Enable public GitHub Pages

1. Push this implementation to `main`.
2. In **Settings → Pages → Build and deployment**, select **GitHub Actions**.
3. Ensure the repository permits the publishing workflow's `contents: write` token to commit `data/added_at.json` to `main`. Branch protection must allow this bot write; otherwise publishing stops before deployment. Do not weaken organization-wide protection just to enable this prototype.
4. Run **Actions → Publish paperlist → Run workflow**, or push a new note.
5. Check the workflow and open its deployment URL. Future pushes to `main` update the site automatically; pull requests only validate.

The publishing workflow tests and validates all content before changing the timestamp ledger. It commits dates before deployment, so failed deployments and subsequent edits cannot reset them. Bot commits made with `GITHUB_TOKEN` do not trigger another push workflow. Publishing is serialized; errors leave the last deployed site intact. The workflow uses the latest `main` so queued pushes are eventually included.

For a protected-branch lab repository, adapt ledger persistence to a dedicated automation branch or another durable store before rollout. This prototype intentionally uses a simple tracked ledger on `main`.

## Structure

```text
config/site.json          Site identity, members, topic vocabulary, weekly target
entries/<member>/*.md     Real reading notes
examples/<member>/*.md    Clearly labeled demonstration notes
templates/paper.md       Submission template
data/added_at.json        Persistent contribution timestamps
scripts/build.py         Validation, safe Markdown rendering, static build
site/                    HTML, CSS, and browser JavaScript
tests/                   Validation, security, and date-regression tests
.github/workflows/       Submission checks and Pages publishing
```

## Moving this to the lab

Update the repository URL, title, members, and topics in `config/site.json`, and remove or retain the isolated examples as desired. The lab repository has not been changed by this prototype.

**This personal site is public.** A private source repository alone does not make GitHub Pages private. Private project Pages require an eligible organization using GitHub Enterprise Cloud; confirm access controls before deploying lab notes. See [GitHub's private Pages documentation](https://docs.github.com/en/enterprise-cloud@latest/pages/getting-started-with-github-pages/changing-the-visibility-of-your-github-pages-site).
