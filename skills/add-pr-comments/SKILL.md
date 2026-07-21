---
name: add-pr-comments
description: Add line-specific review comments on a GitHub Pull Request. Use when the user says "adiciona comentários no PR" or "add comments to the PR" referring to specific review points previously identified.
---

## Tone

Use one of two collaborative tones, choosing the one that best fits the review point. The goal is to make the underlying concern and proposed next step clear without sounding judgmental.

1. **Genuine question:** Use a direct question when you need the author's context or reasoning to evaluate the code, or when there are multiple plausible approaches. For example: "Why did you choose X here?", "Could this cause Z?", or "Would Y also need to change when this value changes?"

2. **Direct suggestion:** When the issue and practical improvement are clear, state the problem and recommendation plainly. Give the comment a natural progression: **observation → consequence → recommended action → invitation to engage**. Make the invitation specific to the suggestion instead of attaching a generic suffix. For example: "This duplicates the validation logic in `src/validators/user.ts`, so the two paths can drift. Could we extract it into a shared helper?" or "Centralizing this validation in `src/validators/user.ts` would keep the behavior consistent. Would that fit the intended ownership of this logic?"

Vary the final invitation across comments. Do not default to or repeatedly reuse **"What do you think?"**. Choose a closing that flows from the recommendation: **"Could we…?"**, **"Would it make sense to…?"**, **"Would you be open to…?"**, **"Does that fit the intended…?"**, **"How does that sound?"**, or, when it is genuinely natural, **"What do you think?"** / **"How about doing that?"**.

Do not turn a clear recommendation into an indirect question just for politeness. Conversely, do not present an uncertain concern as a directive: ask a genuine question when the author's intent or missing context matters. Avoid judgmental phrasing such as "this is wrong".

## Language

This skill is for adding **new** review comments, so write them in the same language used in the PR's title and description (`gh pr view --json title,body`), regardless of the language the user asked in.

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
  -f body="The testID \`user-form-papel-select\` does not exist in the source code, so this scenario cannot find the target element. Would it make sense to check whether it was renamed or removed?" \
  -f commit_id="fcbb2d1946e3e01b35fec9c3fdc688cc2039c1dd" \
  -f path=".maestro/create-user-organizador.yaml" \
  -F line=53 \
  -f side="RIGHT"
```

Multi-line (block) comment:
```
gh api repos/tecMTST/app-vitoria-mobile/pulls/72/comments \
  -f body="This entire block duplicates the validation logic in \`src/validators/user.ts\`, which can cause the two implementations to drift. Could we extract it into a shared helper?" \
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
  -f body="**File: \`src/utils/helpers.ts\` (line 120)** — The \`formatDate\` function appears to be duplicated. Centralizing it in \`src/helpers/date.ts\` would keep the behavior in one place. Would you be open to reusing that version here?"
```

Update existing comment:
```
gh api repos/tecMTST/app-vitoria-mobile/pulls/comments/123456 \
  -X PATCH \
  -f body="The testID \`user-form-papel-select\` does not exist in the source code, so this scenario cannot find the target element. Would it make sense to check whether it was renamed or removed?"
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
