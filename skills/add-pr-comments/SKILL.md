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

3. Extract owner/repo from `git remote get-url origin`.

4. For each comment, use the **file line number** (NOT the diff position). Read the file to confirm the exact line number.

5. Before posting, check if there are already existing review comments on the same file + line:

   ```
   gh api repos/:owner/:repo/pulls/:number/comments
   ```

   Filter the response for comments that match the same `path` and `line`. If one is found:

   - **Compare the content** of the existing comment with the new comment you intend to post.
   - If the existing comment **already fully covers the same point** (mesmo contexto, mesma informação essencial), **skip** — não poste nem atualize.
   - If the existing comment is **incomplete or missing key information**, **update** it with the complete content using `PATCH`:

     ```
     gh api repos/:owner/:repo/pulls/comments/:comment_id \
       -X PATCH \
       -f body="<conteúdo completo, incluindo a informação nova>"
     ```

   - If **no existing comment** is found on that file + line, post a new one as normal.

6. Add each new comment using:
   ```
   gh api repos/:owner/:repo/pulls/:number/comments \
     -f body="..." \
     -f commit_id="<sha>" \
     -f path="<file-path>" \
     -F line=<file-line-number> \
     -f side="RIGHT"
   ```

   Parameters:
   - `body`: the comment text
   - `commit_id`: the SHA from step 2
   - `path`: the file path relative to repo root (e.g. `.maestro/create-user.yaml`)
   - `line`: the 1-indexed file line number (read the file to get it)
   - `side`: always `"RIGHT"` (the new version of the file)

## Example

Novo comentário:
```
gh api repos/tecMTST/app-vitoria-mobile/pulls/72/comments \
  -f body="O testID \`user-form-papel-select\` não existe no código fonte." \
  -f commit_id="fcbb2d1946e3e01b35fec9c3fdc688cc2039c1dd" \
  -f path=".maestro/create-user-organizador.yaml" \
  -F line=53 \
  -f side="RIGHT"
```

Atualizar comentário existente:
```
gh api repos/tecMTST/app-vitoria-mobile/pulls/comments/123456 \
  -X PATCH \
  -f body="O testID \`user-form-papel-select\` não existe no código fonte. Verifique se foi renomeado ou removido."
```

## Notes

- Use `-f` for string values and `-F` for integers/booleans (required for `line`).
- Use `line` (file line number) instead of `position` (diff position). The `position` parameter is deprecated and error-prone — it requires counting diff hunk lines, which is unreliable.
- Owner/repo can be extracted from `git remote get-url origin`.
- To decide if a comment is "complete", check if the existing comment's body contains the same core observation/point as the new comment. If it mentions the same problem but lacks detail, update it. If it already has the same level of detail, skip.
