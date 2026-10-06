#!/usr/bin/env bash
set -euo pipefail
# Runs only in a disposable Actions checkout, serialized with branch rotation.
git config user.name "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
for attempt in 1 2 3; do
  git fetch origin main
  git reset --hard origin/main
  python scripts/index.py --record
  git add README.md catalog data/added_at.json
  if git diff --cached --quiet; then exit 0; fi
  git commit -m "Update paper indexes"
  if git push origin HEAD:main; then exit 0; fi
done
exit 1
