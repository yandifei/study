#!/usr/bin/env python3
"""
Check whether a GitHub user starred a repo.

Usage:
  export GITHUB_TOKEN="ghp_... or github_pat_..."
  python check_star.py --owner octocat --repo Hello-World --user someuser
"""

import os
import argparse
import requests


def has_starred(owner: str, repo: str, user: str, token: str | None = None, timeout: float = 10.0) -> bool:
    """
    Returns True if `user` has starred `owner/repo`, else False.

    Uses:
      GET /users/{username}/starred/{owner}/{repo}

    Response:
      204 -> starred
      404 -> not starred (or not accessible)
    """
    url = f"https://api.github.com/users/{user}/starred/{owner}/{repo}"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        # Optional: helps with conditional requests, but not needed here
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    r = requests.get(url, headers=headers, timeout=timeout)

    if r.status_code == 204:
        return True
    if r.status_code == 404:
        return False

    # Helpful error for other cases: 401, 403 rate-limited, etc.
    msg = f"GitHub API error {r.status_code}: {r.text}"
    raise RuntimeError(msg)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--owner", required=True, help="Repo owner/org, e.g. 'octocat'")
    p.add_argument("--repo", required=True, help="Repo name, e.g. 'Hello-World'")
    p.add_argument("--user", required=True, help="GitHub username to check")
    p.add_argument("--token", default=os.getenv("GITHUB_TOKEN"), help="GitHub token (or set env GITHUB_TOKEN)")
    args = p.parse_args()

    starred = has_starred(args.owner, args.repo, args.user, args.token)
    print("STARRED" if starred else "NOT_STARRED")


if __name__ == "__main__":
    main()
