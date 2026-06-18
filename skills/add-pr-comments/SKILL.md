---
name: add-pr-comments
description: Add line-specific review comments on a GitHub Pull Request. Use when the user says "adiciona comentários no PR" or "add comments to the PR" referring to specific review points previously identified.
---

## Tone

Write every comment as a curious question, not a critique. The goal is to spark dialogue and understanding, not to judge. Frame observations as genuine curiosity about the author's intent — "Why did you choose X here?", "I'm wondering if Y could work here too — what do you think?", "Could this cause Z? Curious what your reasoning was." Avoid declarative statements like "this is wrong" or "you should". If something looks like a bug or a concern, ask about it.

## Steps

1. Identify the PR number with `gh pr view --json number` (or from the branch name / user context).

2. Get the current commit SHA:
   ```
   git rev-parse HEAD
   ```

3. Extract owner/repo from `git remote get-url origin`.

4. For each comment, use **file line numbers** (NOT diff positions). Read the file to confirm the exact line numbers. Decide whether the comment targets a **single line** or a **block of lines**:

   - Use a **single-line comment** for observations that concern exactly one line (e.g., a wrong variable name, a missing semicolon).
   - Use a **multi-line (block) comment** when the observation spans a coherent block — a full function, a conditional branch, a repeated pattern, or any group of lines that must be read together to understand the point. The block must start and end within the same diff hunk.

   When in doubt, prefer the range that gives the reviewer the most context without being unnecessarily wide.

5. Check if the file is in the PR diff:

   ```
   gh api repos/:owner/:repo/pulls/:number/files --jq '.[].filename'
   ```

   If the file path is **NOT in the diff**, post the comment as a **general PR comment** referencing the file and line so the person can locate themselves:

   ```
   gh api repos/:owner/:repo/issues/:number/comments \
     -f body="**File: \`<file-path>\` (line <line-number>)** — <comment>"
   ```

   Then **skip** the following steps (do not attempt to post as a diff comment).

   If the file **is in the diff**, proceed with the steps below.

6. Before posting, check if there are already existing review comments on the same file + line (or overlapping range):

   ```
   gh api repos/:owner/:repo/pulls/:number/comments
   ```

   Filter the response for comments that match the same `path` and whose `line` (or `start_line`–`line` range) overlaps the intended range. If one is found:

   - **Compare the content** of the existing comment with the new comment you intend to post.
   - If the existing comment **already fully covers the same point** (same context, same essential information), **skip** — do not post or update.
   - If the existing comment is **incomplete or missing key information**, **update** it with the complete content using `PATCH`:

     ```
     gh api repos/:owner/:repo/pulls/comments/:comment_id \
       -X PATCH \
       -f body="<complete content, including the new information>"
     ```

   - If **no existing comment** is found on that file + line, post a new one as normal.

7. Add each new comment (only for files that are in the diff).

   **Single-line comment:**
   ```
   gh api repos/:owner/:repo/pulls/:number/comments \
     -f body="..." \
     -f commit_id="<sha>" \
     -f path="<file-path>" \
     -F line=<file-line-number> \
     -f side="RIGHT"
   ```

   **Multi-line (block) comment:**
   ```
   gh api repos/:owner/:repo/pulls/:number/comments \
     -f body="..." \
     -f commit_id="<sha>" \
     -f path="<file-path>" \
     -F start_line=<first-line-of-block> \
     -f start_side="RIGHT" \
     -F line=<last-line-of-block> \
     -f side="RIGHT"
   ```

   Parameters:
   - `body`: the comment text
   - `commit_id`: the SHA from step 2
   - `path`: the file path relative to repo root (e.g. `.maestro/create-user.yaml`)
   - `line`: the last (or only) line of the target range
   - `start_line`: first line of the range — **only for multi-line comments**; omit for single-line
   - `start_side` / `side`: always `"RIGHT"` (the new version of the file)
   - `start_line` must be strictly less than `line`; both must fall within the same diff hunk

## Examples

Single-line comment:
```
gh api repos/tecMTST/app-vitoria-mobile/pulls/72/comments \
  -f body="The testID \`user-form-papel-select\` does not exist in the source code." \
  -f commit_id="fcbb2d1946e3e01b35fec9c3fdc688cc2039c1dd" \
  -f path=".maestro/create-user-organizador.yaml" \
  -F line=53 \
  -f side="RIGHT"
```

Multi-line (block) comment:
```
gh api repos/tecMTST/app-vitoria-mobile/pulls/72/comments \
  -f body="This entire block duplicates the validation logic in \`src/validators/user.ts\`. Extract it into a shared helper to avoid drift." \
  -f commit_id="fcbb2d1946e3e01b35fec9c3fdc688cc2039c1dd" \
  -f path="src/screens/CreateUser.tsx" \
  -F start_line=40 \
  -f start_side="RIGHT" \
  -F line=58 \
  -f side="RIGHT"
```

General PR comment (file not in diff):
```
gh api repos/tecMTST/app-vitoria-mobile/issues/72/comments \
  -f body="**File: \`src/utils/helpers.ts\` (line 120)** — The \`formatDate\` function appears to be duplicated. Consider unifying it with the version in \`src/helpers/date.ts\`."
```

Update existing comment:
```
gh api repos/tecMTST/app-vitoria-mobile/pulls/comments/123456 \
  -X PATCH \
  -f body="The testID \`user-form-papel-select\` does not exist in the source code. Check if it was renamed or removed."
```

## Notes

- **Escape backticks** inside double-quoted `-f body="..."` with `\``, otherwise the shell interprets them as command substitution and strips the content. Exemplo: `-f body="The \`formatDate\` function"`.
- **Multi-line comments require both lines in the same hunk.** If `start_line` and `line` cross a hunk boundary the API returns a 422. If that happens, fall back to a single-line comment on the last line of the block.
- **Use `-F` (uppercase)** for all numeric fields (`start_line`, `line`); use `-f` (lowercase) for strings (`start_side`, `side`, `body`, etc.).
- Use `-f` for string values and `-F` for integers/booleans (required for `line`).
- Use `line` (file line number) instead of `position` (diff position). The `position` parameter is deprecated and error-prone — it requires counting diff hunk lines, which is unreliable.
- Owner/repo can be extracted from `git remote get-url origin`.
- To decide if a comment is "complete", check if the existing comment's body contains the same core observation/point as the new comment. If it mentions the same problem but lacks detail, update it. If it already has the same level of detail, skip.
- To check if a file is in the diff, use `gh api repos/:owner/:repo/pulls/:number/files --jq '.[].filename'` and verify the file path appears in the list.
- General PR comments (issue comments) are not tied to a specific line but are useful for files that were not changed in the PR. Always include the file path and line in the body for reference.

## Post-submission validation

After posting all comments, **validate each one** by reading back the response JSON or fetching the comment:

1. **Line number**: confirm the `line` field in the response matches the intended line (the `-F line=` value you sent).
2. **File path**: confirm the `path` field matches the intended file.
3. **Body content**: confirm the `body` field preserved all text, especially text inside backticks — if backticks were not escaped, the content may be missing.
4. **No duplicate comments**: if you accidentally posted the same comment twice, delete the duplicate with `gh api repos/:owner/:repo/pulls/comments/:id -X DELETE`.

If any comment is wrong, **delete and re-post** it with the correct parameters.
