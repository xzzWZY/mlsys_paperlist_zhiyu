#!/usr/bin/env python3
"""Create the next submission branch after a same-repository submission PR merges."""
from datetime import datetime, timedelta
import json
import os
from pathlib import Path
import re
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo


def next_branch(event, repository, enabled=True):
    pr = event.get('pull_request', {})
    head = pr.get('head', {})
    if (not enabled or event.get('action') != 'closed' or not pr.get('merged')
            or pr.get('base', {}).get('ref') != 'main'
            or head.get('repo', {}).get('full_name') != repository
            or not re.fullmatch(r'submissions/\d{4}-\d{2}-\d{2}_to_\d{4}-\d{2}-\d{2}', head.get('ref', ''))):
        return None
    # Use merge time so retries on another date retain the same branch name.
    start = datetime.fromisoformat(pr['merged_at'].replace('Z', '+00:00')).astimezone(ZoneInfo('America/Chicago')).date()
    end = start + timedelta(days=(7 - start.weekday()) % 7 or 7)
    return f'submissions/{start.isoformat()}_to_{end.isoformat()}'


def create_branch(api, repository, branch):
    prefix = f'/repos/{repository}/git'
    existing = api('GET', f'{prefix}/ref/heads/{branch}', missing_ok=True)
    if existing:
        return 'already exists; left unchanged'
    latest = api('GET', f'{prefix}/ref/heads/main')['object']['sha']
    try:
        api('POST', f'{prefix}/refs', {'ref': f'refs/heads/{branch}', 'sha': latest})
    except HTTPError as exc:
        if exc.code != 422 or not api('GET', f'{prefix}/ref/heads/{branch}', missing_ok=True):
            raise
        return 'already exists; left unchanged'
    return f'created from main at {latest}'


def api(method, path, payload=None, missing_ok=False):
    request = Request(os.environ.get('GITHUB_API_URL', 'https://api.github.com') + path,
                      data=json.dumps(payload).encode() if payload is not None else None,
                      headers={'Authorization': f'Bearer {os.environ["GH_TOKEN"]}',
                               'Accept': 'application/vnd.github+json', 'Content-Type': 'application/json'},
                      method=method)
    try:
        with urlopen(request, timeout=30) as response:
            return json.load(response)
    except HTTPError as exc:
        if missing_ok and exc.code == 404:
            return None
        raise


if __name__ == '__main__':
    event = json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_text())
    repository = os.environ['GITHUB_REPOSITORY']
    branch = next_branch(event, repository, os.environ.get('AUTO_CREATE_SUBMISSION_BRANCH', 'true').lower() != 'false')
    if branch:
        message = f'{branch}: {create_branch(api, repository, branch)}'
        print(message)
        if os.environ.get('GITHUB_STEP_SUMMARY'):
            with open(os.environ['GITHUB_STEP_SUMMARY'], 'a') as summary:
                summary.write(f'Next submission branch: `{message}`\n')
    else:
        print('No eligible merged submission PR, or automation disabled.')
