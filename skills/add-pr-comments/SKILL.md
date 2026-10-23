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

4. Prepare a posting plan with one entry per finding: its classification, the best relevant changed line or range, and its comment channel. Each in-scope finding must map to its own dedicated comment; never combine multiple in-scope findings in one comment body. Finding identifiers (for example `BR-001`) are internal conversation tools only: never include them in posted PR content. Use the finding title without its identifier, and do not add mapping tables or parenthetical references to identifiers:
   - **In-scope:** prioritize these findings and draft one detailed comment per finding, following `pr-comment-writing`. Inspect the PR diff and post each finding as its own inline review comment on the most relevant changed line or smallest coherent range within one diff hunk. Treat finding an anchor as part of the required work; a finding being described in prose without a proposed location is not a reason to use a general comment. Use a general PR comment for an in-scope finding only when no meaningful line or range in the PR diff can host it. If the selected backend has no inline-comment operation, use a separate general comment per finding when its guide supports that fallback; otherwise report the missing capability. Include the best available file or area reference in each general comment. Keep in-scope findings out of the out-of-scope summary.
   - **Out-of-scope and follow-up:** combine all unacknowledged findings in these categories into one brief, informational review summary; do not create an individual comment for each. Include a short introduction and one distinct impact bullet per finding, labeling each item, for example `- [Out of scope] Issue: brief impact.` or `- [Follow-up] Issue: brief impact.` Label unresolved scope decisions `[Scope unclear]`. Keep the summary for the author's awareness and optional further exploration, without asking for the issue to be fixed in this PR.
   - If there are no findings in a group, omit that group's comments.

5. Keep the channels distinct: inline threads or separate general PR comments carry in-scope findings, one finding per comment; the review-level body carries only the out-of-scope/follow-up summary, with one distinct bullet per finding. If that summary has items, put it in the review-level body when supported, preferably in the same review submission as the in-scope inline comments. Do not put in-scope findings into the review-level body or combine them with the summary in a general comment. Use a comment-only review state when a state is required; the summary alone does not approve the PR or request changes. If review-level bodies are unavailable, post exactly one general PR comment containing only the summary.

6. Before posting, check for an existing dedicated comment for each in-scope finding on the same file and line or overlapping range. A shared review body or general comment that groups multiple in-scope findings does not satisfy the one-comment-per-finding requirement. Reuse a dedicated comment only when it fully covers that finding; update an incomplete dedicated comment when the environment guide supports it, and report when a required update is unavailable. Also check existing review bodies and general PR comments for the out-of-scope summary; update a matching summary instead of duplicating it when possible.

7. Before each create or update, draft the complete body. Verify the draft contains no finding identifier. Add the AI-disclosure signature required by `pr-comment-writing` after a blank line to every new in-scope comment and to the out-of-scope summary, whether it is in a review body or a general PR comment. Ensure the submitted body contains a real line break there.

8. Post the in-scope comments and the out-of-scope summary using the selected environment guide. Verify one-to-one coverage: every in-scope finding has its own dedicated inline comment or, when inline is unavailable, its own general PR comment. Verify each inline comment's file path and line or range, and that the review summary has a distinct bullet for every unacknowledged out-of-scope, follow-up, or scope-unclear finding. Confirm that no finding identifier leaked into posted content and that the AI disclosure and its line break were preserved. Correct errors using the environment's edit or delete-and-repost operations; report any capability gap that prevents complete coverage.
