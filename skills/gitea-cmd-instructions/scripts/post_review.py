#!/usr/bin/env python3
"""Post inline review comments on a Gitea pull request via the tea CLI.

Gitea has no dedicated `tea` subcommand for inline (diff-line) comments, so
this helper builds the `POST /repos/{owner}/{repo}/pulls/{index}/reviews`
payload from a JSON file and posts it with `tea api`. Bodies are read from
files, never from shell arguments, so backticks, quotes, and newlines in
AI-drafted comments cannot break shell quoting.

Batch input (recommended). The agent writes this file with its file-writing
tool (no shell quoting involved), then runs this script:

    [
      {"path": "app.json", "line": 11, "body": "Why was this bumped?"},
      {"path": "app/api/ApiClient.ts", "line": 10, "side": "new",
       "body": "Could this reuse the shared constant?"}
    ]

Each entry requires `path` (repo-root-relative, exactly as shown in the PR
diff), `line` (1-based file line number, integer), and `body` (non-empty).
`side` is optional: "new" (default, added/changed line on the RIGHT side) or
"old" (removed line on the LEFT side).

Examples:
    # Batch of inline comments in one review request:
    python3 post_review.py --repo owner/repo --pr 4 \\
        --comments-file comments.json --review-body "AI review notes"

    # Single inline comment, body read from a file:
    python3 post_review.py --repo owner/repo --pr 4 \\
        --path app.json --line 11 --body-file comment.md

    # Validate without posting:
    python3 post_review.py --repo owner/repo --pr 4 \\
        --comments-file comments.json --dry-run
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def run_tea(args: list[str]) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            ["tea", *args], text=True, capture_output=True, check=False
        )
    except FileNotFoundError:
        sys.exit("error: `tea` CLI not found on PATH. Install tea first.")


def tea_base_args(repo: str | None, login: str | None) -> list[str]:
    base: list[str] = []
    if repo:
        base += ["--repo", repo]
    if login:
        base += ["-l", login]
    return base


def fetch_head_sha(repo: str | None, login: str | None, pr: int) -> str:
    result = run_tea(
        ["api", f"repos/{{owner}}/{{repo}}/pulls/{pr}", *tea_base_args(repo, login)]
    )
    if result.returncode:
        sys.exit(f"error: could not fetch PR {pr}: {result.stderr.strip()}")
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        sys.exit(f"error: unexpected response fetching PR {pr}: {result.stdout[:500]}")
    sha = (data.get("head") or {}).get("sha", "")
    if not sha:
        sys.exit(f"error: PR {pr} response has no head.sha; is the PR index correct?")
    return sha


def fetch_diff_filenames(
    repo: str | None, login: str | None, pr: int
) -> set[str] | None:
    result = run_tea(
        [
            "api",
            f"repos/{{owner}}/{{repo}}/pulls/{pr}/files",
            *tea_base_args(repo, login),
        ]
    )
    if result.returncode:
        return None  # non-fatal: skip the check, let the API validate
    try:
        files = json.loads(result.stdout)
    except json.JSONDecodeError:
        return None
    return {f.get("filename", "") for f in files if f.get("filename")}


def load_comments(args: argparse.Namespace) -> list[dict]:
    if args.comments_file:
        try:
            raw = json.loads(Path(args.comments_file).read_text(encoding="utf-8"))
        except FileNotFoundError:
            sys.exit(f"error: comments file not found: {args.comments_file}")
        except json.JSONDecodeError as exc:
            sys.exit(f"error: comments file is not valid JSON: {exc}")
        if not isinstance(raw, list) or not raw:
            sys.exit("error: comments file must be a non-empty JSON array.")
        return raw
    # Single-comment mode.
    if args.body_file:
        body = Path(args.body_file).read_text(encoding="utf-8").strip()
    else:
        body = (args.body or "").strip()
    if not args.path or not args.line or not body:
        sys.exit(
            "error: single-comment mode needs --path, --line, and "
            "--body-file (or --body)."
        )
    return [
        {"path": args.path, "line": args.line, "side": args.side, "body": body}
    ]


def normalize_comments(raw: list[dict]) -> list[dict]:
    normalized: list[dict] = []
    for i, entry in enumerate(raw):
        if not isinstance(entry, dict):
            sys.exit(f"error: comment #{i + 1} must be an object.")
        path = str(entry.get("path", "")).strip()
        body = str(entry.get("body", "")).strip()
        side = str(entry.get("side", "new") or "new").lower()
        try:
            line = int(entry.get("line", 0))
        except (TypeError, ValueError):
            sys.exit(f"error: comment #{i + 1} has a non-integer line.")
        if not path or path.startswith("/"):
            sys.exit(
                f"error: comment #{i + 1} needs a repo-root-relative `path` "
                "without a leading `/` (exactly as shown in the PR diff)."
            )
        if line <= 0:
            sys.exit(f"error: comment #{i + 1} needs a positive `line` number.")
        if side not in ("new", "old"):
            sys.exit(f"error: comment #{i + 1} `side` must be 'new' or 'old'.")
        if not body:
            sys.exit(f"error: comment #{i + 1} has an empty `body`.")
        if side == "new":
            normalized.append(
                {
                    "body": body,
                    "path": path,
                    "new_position": line,
                    "old_position": 0,
                }
            )
        else:
            normalized.append(
                {
                    "body": body,
                    "path": path,
                    "new_position": 0,
                    "old_position": line,
                }
            )
    return normalized


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", help="Gitea slug, e.g. app-da-vitoria/app-vitoria-mobile")
    parser.add_argument("--login", "-l", help="tea login name, e.g. git.mtst.tec.br")
    parser.add_argument("--pr", type=int, required=True, help="pull request index")
    parser.add_argument(
        "--commit-id",
        help="PR head SHA. When omitted, it is fetched from the PR (recommended).",
    )
    parser.add_argument(
        "--comments-file",
        help="JSON array file with {path, line, body, [side]} entries.",
    )
    parser.add_argument("--path", help="single-comment mode: file path in the diff")
    parser.add_argument("--line", type=int, help="single-comment mode: 1-based line")
    parser.add_argument(
        "--side",
        default="new",
        choices=["new", "old"],
        help="single-comment mode: new = added/changed line (default), old = removed line",
    )
    parser.add_argument("--body", help="single-comment mode: comment text (short only)")
    parser.add_argument(
        "--body-file", help="single-comment mode: file holding the comment text"
    )
    parser.add_argument("--review-body", default="", help="summary text of the review")
    parser.add_argument(
        "--review-body-file", help="file holding the review summary text"
    )
    parser.add_argument(
        "--skip-file-check",
        action="store_true",
        help="skip verifying that each path is in the PR diff",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print the review payload without posting it",
    )
    parser.add_argument(
        "--payload-file", help="also write the review payload JSON to this path"
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    raw = load_comments(args)
    comments = normalize_comments(raw)

    commit_id = args.commit_id or fetch_head_sha(args.repo, args.login, args.pr)

    if not args.skip_file_check:
        filenames = fetch_diff_filenames(args.repo, args.login, args.pr)
        if filenames is not None:
            missing = sorted({c["path"] for c in comments} - filenames)
            if missing:
                sys.exit(
                    "error: path(s) not in the PR diff: "
                    + ", ".join(missing)
                    + ". Post those as general PR comments "
                    "(tea comments add) instead, or re-check the filename."
                )

    if args.review_body_file:
        review_body = Path(args.review_body_file).read_text(encoding="utf-8").strip()
    else:
        review_body = args.review_body.strip()

    payload = {
        "body": review_body,
        "event": "COMMENT",
        "commit_id": commit_id,
        "comments": comments,
    }
    payload_text = json.dumps(payload, ensure_ascii=False, indent=2)

    if args.payload_file:
        Path(args.payload_file).write_text(payload_text + "\n", encoding="utf-8")

    if args.dry_run:
        print(payload_text)
        return 0

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(payload_text)
        tmp_path = tmp.name

    result = run_tea(
        [
            "api",
            f"repos/{{owner}}/{{repo}}/pulls/{args.pr}/reviews",
            *tea_base_args(args.repo, args.login),
            "-d",
            f"@{tmp_path}",
        ]
    )
    if result.returncode:
        sys.exit(
            "error: tea api failed:\n"
            f"{result.stderr.strip()}\n{result.stdout.strip()}\n"
            "Common causes: stale --commit-id (omit the flag to auto-fetch), "
            "a line outside the diff hunk, or a path not in the diff."
        )
    try:
        review = json.loads(result.stdout)
    except json.JSONDecodeError:
        sys.exit(f"error: unexpected API response: {result.stdout[:1000]}")
    print(
        json.dumps(
            {
                "review_id": review.get("id"),
                "state": review.get("state"),
                "comments_count": review.get("comments_count"),
                "commit_id": review.get("commit_id"),
                "html_url": review.get("html_url"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    print(
        f"Verify with: tea pulls review-comments {args.pr}",
        end="",
    )
    if args.repo:
        print(f" --repo {args.repo}", end="")
    if args.login:
        print(f" -l {args.login}", end="")
    print(" -o json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
