---
name: add-pr-comments
description: Add line-specific review comments on a GitHub Pull Request. Use whenever the user wants to post review comments on a PR — triggers include "adiciona comentários no PR", "comentar no PR", "add comments to the PR", "post review comments", "adicionar review no PR", referring to specific findings previously identified.
---

# Add comments to a pull request

## Choose the environment guide

Read the guide for the GitHub access method available in the current environment before gathering PR data or posting comments:

- When the authenticated GitHub CLI (`gh`) is available, follow [`references/github-cli.md`](references/github-cli.md).
- When GitHub MCP tools are the available GitHub access method, follow [`references/github-mcp.md`](references/github-mcp.md).
- When both are available, use the method requested by the user or already active in the environment.

Use one guide for the operation and follow its instructions for the tool-specific requests and parameters.

## Shared process

1. Load and follow `pr-comment-writing` before drafting or posting any comment. Use the active GitHub access method to read the PR title and description when choosing the comment language.

2. Identify the PR and inspect its current state, including its head commit, changed files, diff, and existing review comments, using the selected environment guide.

3. For each finding, confirm the file path and current file line number. Use a single-line comment when the observation concerns one line. Use a block comment when the point spans a coherent group of lines that should be read together; keep the range within one diff hunk. When the target file is not in the PR diff, use a general PR comment that names the file and line so the author can locate it.

4. Before posting, check for an existing review comment on the same file and line or an overlapping range. Compare the substance: skip a comment that already covers the same point, and update an incomplete comment with the missing information. Use the environment guide's available update operation.

5. Draft the complete comment, including the AI disclosure required by `pr-comment-writing`, before sending it. Keep a blank line before the disclosure signature and ensure the submitted body contains a real line break there.

6. Post new comments using the selected environment guide. After posting, verify each result's body, file path, and line or range, including the AI disclosure and its line break. If a comment was posted with incorrect content or location, correct it using the environment's edit or delete-and-repost operations.
