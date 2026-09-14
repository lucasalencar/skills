---
name: gitea-cmd-instructions
description: Work efficiently with Gitea via the tea CLI, especially posting inline PR review comments. Use whenever the user wants to comment on a Gitea PR — triggers include "gitea", "tea", "comentar no PR", "adicionar comentário no PR", "add comment to Gitea PR", "inline comment", "comentário em linha", "review comment on Gitea".
---

# Gitea CLI instructions

Use `tea` for all Gitea operations. `tea` has two distinct comment systems —
mixing them up is the most common source of failure.

- **General (issue-level) comments**: visible at the bottom of the PR timeline,
  not attached to any line. Managed with `tea comments`.
- **Inline (review) comments**: attached to a specific file + line in the diff.
  Managed with `tea api` against the pull-review endpoint. There is **no**
  dedicated `tea` subcommand for creating them.

If the user asks for "a comment on line X", they mean an inline comment.
Do NOT use `tea comments add` for that — it will silently post a general
comment instead.

## Prerequisites

1. Confirm the login exists:
   ```
   tea logins
   ```
2. Every command below needs a repo context. Prefer the explicit flags so the
   skill works from any directory:
   ```
   --repo <owner>/<repo> -l <login-name>
   ```
   Example slug: `--repo app-da-vitoria/app-vitoria-mobile`.
   Example login: `-l git.mtst.tec.br`.
3. Load and follow `pr-comment-writing` before drafting any comment body
   (tone, language, AI disclosure).

## Steps — single inline comment on one diff line

This is the core workflow. It was validated end-to-end on
`app-da-vitoria/app-vitoria-mobile` PR 4.

1. Identify the PR index (from the URL or user context) and fetch its head SHA:
   ```
   tea pulls <index> --repo <owner>/<repo> -l <login> -o json --fields index,title,state,author,base,head
   ```
   Or via the API:
   ```
   tea api 'repos/{owner}/{repo}/pulls/<index>' --repo <owner>/<repo> -l <login>
   ```
   Record `head.sha` (e.g. `a193607...`). This value becomes `commit_id`.
   Do NOT use `merge_base` or a local `git rev-parse HEAD` unless the local
   branch exactly matches the PR head.

2. Verify the file is in the PR diff:
   ```
   tea api 'repos/{owner}/{repo}/pulls/<index>/files' --repo <owner>/<repo> -l <login>
   ```
   Match `filename` exactly (e.g. `app.json`, `app/api/ApiClient.ts`).
   If the path is NOT in the list, stop — post a general comment instead
   (see "General comments" below) referencing file + line in the body.

3. Confirm the exact **new-file line number**. Read the file at the PR head
   (`tea api 'repos/{owner}/{repo}/contents/<path>?ref=<head-sha>'`) or the
   raw diff (`tea api 'repos/{owner}/{repo}/pulls/<index>.diff'`). Target a
   changed/added line. Example: `app.json` line `11`
   (`"version": "2.7.2"`) in PR 4.

4. Check for existing inline comments to avoid duplicates:
   ```
   tea pulls review-comments <index> --repo <owner>/<repo> -l <login> -o json
   ```
   Filter by matching `path` and `line`. If an existing comment already makes
   the same point, skip. If it is incomplete, reply to it (see "Replies")
   instead of posting a duplicate.

5. Write the comments to a JSON file with the file-writing tool (never via
   shell interpolation — bodies contain backticks, quotes, and newlines that
   break shell quoting). Format — one object per inline comment:

   ```
   [
     {"path": "<exact filename from step 2>", "line": <new-file line number>,
      "body": "<comment body + AI signature>"},
     {"path": "app/api/ApiClient.ts", "line": 10, "side": "new",
      "body": "<second comment body + AI signature>"}
   ]
   ```

   Rules per entry:
   - `path`: repo-root-relative, no leading `/`, exactly as shown in the diff.
   - `line`: positive integer, 1-based file line number.
   - `body`: non-empty comment text.
   - `side`: optional — `"new"` (default, added/changed line on the RIGHT
     side) or `"old"` (removed line on the LEFT side).
   - One inline comment = one array element. A "single comment on a specific
     line" is an array with exactly one element.

6. Post with the skill helper `scripts/post_review.py` (located next to this
   file — resolve `<skill-dir>` to this skill's directory first, e.g. by
   globbing for `gitea-cmd-instructions`). It builds the review payload from
   the JSON file and posts it with `tea api`, so bodies never pass through
   the shell:

   ```
   # Validate first (prints the payload, posts nothing):
   python3 <skill-dir>/scripts/post_review.py \
     --repo <owner>/<repo> -l <login> --pr <index> \
     --comments-file /tmp/gitea-comments.json \
     --review-body "<short review summary>" --dry-run

   # Post for real:
   python3 <skill-dir>/scripts/post_review.py \
     --repo <owner>/<repo> -l <login> --pr <index> \
     --comments-file /tmp/gitea-comments.json \
     --review-body "<short review summary>"
   ```

   The helper auto-fetches the head SHA (no stale `commit_id`), verifies every
   `path` is in the PR diff (fail-fast with a hint to use a general comment
   instead), and prints the created `review_id`. Single-comment shortcut
   (body read from a file, no `--comments-file` needed):

   ```
   python3 <skill-dir>/scripts/post_review.py \
     --repo <owner>/<repo> -l <login> --pr <index> \
     --path <filename> --line <line> --body-file /tmp/gitea-comment.md
   ```

   Manual fallback (without the helper): build the payload with
   `python3 + json.dumps` into `/tmp/gitea-review.json`
   (`{"body": ..., "event": "COMMENT", "commit_id": "<head-sha>",
   "comments": [{"body": ..., "path": ..., "new_position": <line>,
   "old_position": 0}]}` — `new_position=<line>, old_position=0` for
   added/changed lines, `new_position=0, old_position=<line>` for removed
   lines) and post it:

   ```
   tea api 'repos/{owner}/{repo}/pulls/<index>/reviews' \
     --repo <owner>/<repo> -l <login> \
     -d @/tmp/gitea-review.json -i
   ```

   Expect `200 OK` with a review object (`id`, `state: COMMENT`,
   `comments_count: N`). The `-d` flag implies POST.

7. Validate (see "Post-submission validation" below).

## Steps — multiple inline comments efficiently

Post all comments in **one review request**, not one request per comment:
write all entries into the same JSON file and run the helper once. One
review per batch keeps the PR timeline clean and halves the round-trips.

```
# /tmp/gitea-comments.json (written with the file-writing tool):
[
  {"path": "app.json", "line": 11,
   "body": "note 1 ..."},
  {"path": "app/api/ApiClient.ts", "line": 10,
   "body": "note 2 ..."},
  {"path": "app/contexts/ApiContext.tsx", "line": 120,
   "body": "note 3 ..."}
]
```

```
python3 <skill-dir>/scripts/post_review.py \
  --repo <owner>/<repo> -l <login> --pr <index> \
  --comments-file /tmp/gitea-comments.json \
  --review-body "AI review: 3 inline notes"
```

## Examples

Single inline comment via the helper (validated twice on PR 4, deleted
afterwards — backticks and double quotes in the body survived intact):

```
# 1. /tmp/gitea-comments.json (written with the file-writing tool):
[
  {"path": "app.json", "line": 11,
   "body": "TEST inline comment - will be deleted"}
]

# 2. dry-run (auto-fetches head SHA a1936079..., posts nothing):
python3 <skill-dir>/scripts/post_review.py \
  --repo app-da-vitoria/app-vitoria-mobile -l git.mtst.tec.br --pr 4 \
  --comments-file /tmp/gitea-comments.json \
  --review-body "AI test comment - will be deleted" --dry-run

# 3. post:
python3 <skill-dir>/scripts/post_review.py \
  --repo app-da-vitoria/app-vitoria-mobile -l git.mtst.tec.br --pr 4 \
  --comments-file /tmp/gitea-comments.json \
  --review-body "AI test comment - will be deleted"
# -> {"review_id": 780, "state": "COMMENT", "comments_count": 1, ...}

# 4. verify:
tea pulls review-comments 4 --repo app-da-vitoria/app-vitoria-mobile \
  -l git.mtst.tec.br -o json
# -> [{"id": "3234", "path": "app.json", "line": "11", "body": "TEST ...", ...}]

# 5. clean up test:
tea api 'repos/{owner}/{repo}/pulls/4/reviews/780' \
  --repo app-da-vitoria/app-vitoria-mobile -l git.mtst.tec.br -X DELETE -i
# -> 204 No Content
```

## General comments (not attached to a line)

Use only when the file is NOT in the diff, or the note is PR-wide:

```
tea comments add <index> --repo <owner>/<repo> -l <login> \
  -d "$body"
```

List them:

```
tea comments list <index> --repo <owner>/<repo> -l <login> -o json
tea pulls review-comments <index> --repo <owner>/<repo> -l <login> -o json
```

The first lists general comments; the second lists inline comments.
Neither lists the other type — check both when deduplicating.

## Replies, edit, delete, resolve

Reply to an existing inline thread (preferred over duplicating):

```
tea pulls reply <index> <comment-id> --repo <owner>/<repo> -l <login> \
  -d "$body"
# or: tea api 'repos/{owner}/{repo}/pulls/<index>/comments/<comment-id>/replies' -d @reply.json
```

Edit a general comment:

```
tea comments edit <comment-id> --repo <owner>/<repo> -l <login> -d "$new_body"

```
Delete a whole review (removes its inline comments too):

```
tea api 'repos/{owner}/{repo}/pulls/<index>/reviews/<review-id>' \
  --repo <owner>/<repo> -l <login> -X DELETE -i
```

Resolve / unresolve an inline thread:

```
tea pulls resolve <comment-id> --repo <owner>/<repo> -l <login>
tea pulls unresolve <comment-id> --repo <owner>/<repo> -l <login>
```

## Notes

- **Gitea inline comments are single-point, not ranged.** Unlike GitHub
  (`start_line`/`line`), `CreatePullReviewComment` accepts only
  `new_position` / `old_position` — one line per comment. To cover a block,
  post on the last line of the block and name the range in the body
  (e.g. "Lines 40–58: ...").
- **`commit_id` is mandatory.** Omitting it or sending a stale SHA yields
  `422`. Always re-fetch the head SHA right before posting.
- **The line must belong to the diff.** Commenting on an unchanged line far
  outside any hunk fails. Fall back to a general comment with a
  `File: <path> (line N)` prefix.
- **Never pass comment bodies through the shell.** Write `comments.json`
  (and any `--body-file`) with the file-writing tool and let
  `scripts/post_review.py` read them — backticks, double quotes, and literal
  `\n` in AI-drafted bodies survive intact. The manual `-d @file` fallback
  requires building the payload with `python3 + json.dumps`, never with
  shell interpolation.
- **Quote endpoints containing `?` or `&`.** Example:
  `'repos/{owner}/{repo}/contents/app.json?ref=<sha>'`.
- **`{owner}` / `{repo}` placeholders** in `tea api` endpoints are filled
  from `--repo <owner>/<repo>` — keep both, do not hardcode one and omit
  the other.
- **`tea pulls review` is interactive.** Never invoke it from a subagent —
  it blocks waiting for a TTY. Use the non-interactive `tea api` flow above.
- AI disclosure: append the signature from `pr-comment-writing`
  (e.g. `— comment generated with <tool> (<model>)`) after a blank line at
  the end of each `comments[].body`.

## Common errors

- **"Used `tea comments add`, comment appeared at the bottom, not on the
  line"** — expected: that subcommand only creates general comments. Re-post
  via `POST .../pulls/<index>/reviews` as shown above.
- **`404 path not in diff`** — the `path` is misspelled or the file is not in
  `pulls/<index>/files`. Re-check the exact `filename`.
- **`422 Validation failed`** — usually a stale `commit_id`, a line outside
  the diff hunk, or a missing `event: COMMENT`. Re-fetch head SHA and confirm
  the line is added/changed.
- **`422 new_position / old_position both 0`** — one of them must be nonzero.
  Added line: `new_position=N, old_position=0`. Removed line:
  `new_position=0, old_position=N`.
- **Body shows literal `\n` or drops `` `code` `` segments** — the body went
  through shell interpolation instead of a file. Write `comments.json` with
  the file-writing tool and post via `scripts/post_review.py`.
- **Helper says "path(s) not in the PR diff"** — the `path` is misspelled or
  the file is genuinely not in `pulls/<index>/files`. Post those notes as
  general comments (`tea comments add`) with a `File: <path> (line N)`
  prefix, or pass `--skip-file-check` only when certain the API will accept
  the line.
- **"No login matched, falling back"** — harmless in single-login setups, but
  pass `-l <login>` explicitly when several logins exist.

## Post-submission validation

After every POST, verify — do not assume success from exit code alone:

1. **Status**: `-i` output must show `200 OK` (create) or `204` (delete).
2. **Line + path**: fetch back and compare:
   ```
   tea pulls review-comments <index> --repo <owner>/<repo> -l <login> -o json
   tea api 'repos/{owner}/{repo}/pulls/<index>/reviews/<review-id>/comments' \
     --repo <owner>/<repo> -l <login>
   ```
   Confirm `path` and `line` equal the intended values and `body` preserved
   backticks with real line breaks.
3. **No duplicates**: if the same body was posted twice, delete the extra
   review with `DELETE .../pulls/<index>/reviews/<review-id>`.
4. **Clean up tests**: any validation comment posted during development must
   be deleted before finishing, so the PR timeline stays clean.
