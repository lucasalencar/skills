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

1. Load and follow `pr-comment-writing` before drafting or posting. Use the active GitHub access method to read the PR title and description when choosing the comment language.

2. Identify the PR and inspect its current state, including its head commit, changed files, diff, and existing review comments, using the selected environment guide.

3. Read the findings from the branch review and preserve their scope classifications. If findings lack classifications, load and follow `branch-review-scope` to classify them from the task and PR context. Cross-check them against the PR description: when it explicitly identifies the same behavior or gap as out-of-scope or deferred, classify it as **out-of-scope (acknowledged)**. Exclude acknowledged issues from every PR comment, including the consolidated summary, because the author has already documented them. A related or generic mention is not enough; if the review finds a conflict with an explicit requirement or a new concrete impact beyond what the description covers, handle that new finding normally. Keep other unresolved scope decisions labeled as such; do not assume they are in-scope.

4. Prepare comments by classification:
   - **In-scope:** prioritize these findings and draft one detailed comment per finding, following `pr-comment-writing`. When a valid diff line or coherent range can host the comment, anchor it directly to the impacted code. If the finding has no code line to attach to, or the impacted file or line cannot host an inline comment, post a detailed general PR comment for that finding and include the best available file or area reference.
   - **Out-of-scope and follow-up:** combine all unacknowledged findings in these categories into one brief, informational summary; do not create an individual comment for each. Include a short introduction and one brief impact bullet per finding, labeling each item, for example `- [Out of scope] Issue: brief impact.` or `- [Follow-up] Issue: brief impact.` Label unresolved scope decisions `[Scope unclear]`. Keep the summary for the author's awareness and optional further exploration, without asking for the issue to be fixed in this PR.
   - If there are no findings in a group, omit that group's comments.

5. If the out-of-scope summary has items, put it in the review-level body when the selected method supports submitting a review with a body. Prefer to submit it as the body of the same review that contains the in-scope inline comments, and do not post a second general comment with the same summary. Use a comment-only review state when a state is required; the summary alone does not approve the PR or request changes. If review-level bodies are unavailable, post exactly one general PR comment containing the summary.

6. Before posting, check for existing comments that cover each in-scope finding on the same file and line or overlapping range. Also check existing review bodies and general PR comments for the out-of-scope summary. If existing content fully covers the same point or list, skip it. If it is incomplete, update it with the complete content using the environment guide's available operation. When the backend cannot update an incomplete item, do not create a duplicate; report the unavailable update.

7. Before each create or update, draft the complete body. Add the AI-disclosure signature required by `pr-comment-writing` after a blank line to every new in-scope comment and to the out-of-scope summary, whether it is in a review body or a general PR comment. Ensure the submitted body contains a real line break there.

8. Post the in-scope comments and the single out-of-scope summary using the selected environment guide. Verify each result's body and, for inline comments, file path and line or range. Confirm that the AI disclosure and its line break were preserved. Correct errors using the environment's edit or delete-and-repost operations.
