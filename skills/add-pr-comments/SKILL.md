---
name: add-pr-comments
description: Add line-specific review comments on a GitHub Pull Request. Use when the user says "adiciona comentários no PR" or "add comments to the PR" referring to specific review points previously identified.
---

## Steps

1. Identify the PR number with `gh pr view --json number` (or from the branch name / user context).

2. Get the current commit SHA:
   ```
   git rev-parse HEAD
   ```

3. For each comment, determine the `position` (1-indexed line in the diff hunk, NOT the file line number):
   - Run `git diff main...HEAD -- <file-path>` to see the diff
   - The `@@ -start,count +start,count @@` hunk header starts counting at 1 for the first line after it
   - Count each line in the diff output (prefixed with ` `, `+`, or `-`) sequentially within the hunk
   - For new files, position equals the line number in the file (since every line is an addition)

4. Add each comment using:
   ```
   gh api repos/:owner/:repo/pulls/:number/comments \
     -f body="..." \
     -f commit_id="<sha>" \
     -f path="<file-path>" \
     -F position=<N>
   ```

   Parameters:
   - `body`: the comment text
   - `commit_id`: the SHA from step 2
   - `path`: the file path relative to repo root (e.g. `.maestro/create-user.yaml`)
   - `position`: the 1-indexed line position in the diff hunk

## Example

```
gh api repos/tecMTST/app-vitoria-mobile/pulls/72/comments \
  -f body="O testID \`user-form-papel-select\` não existe no código fonte." \
  -f commit_id="fcbb2d1946e3e01b35fec9c3fdc688cc2039c1dd" \
  -f path=".maestro/create-user-organizador.yaml" \
  -F position=53
```

## Notes

- Use `-f` for string values and `-F` for integers/booleans (required for the `position` parameter).
- All files in this context are new, so position equals file line number.
- For existing files with modifications, count positions from the `@@` hunk header.
- Owner/repo can be extracted from `git remote get-url origin`.
