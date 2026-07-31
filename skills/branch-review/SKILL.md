---
name: branch-review
description: Reviews branch changes by running pr-review and assess-change-impact in parallel subagents. Use when asked to review a branch, do a full review before merge, or check what a branch changes and what it might break.
---

Call every applicable skill below, each in its own subagent, following the globally specified guidelines. This applies identically on every invocation of this skill — first call or the tenth in a row within a loop: never skip, merge, or substitute any applicable one.

- `pr-review` — always
- `assess-change-impact` — always
- `code-review` — only when the current client is Claude Code; it does not exist elsewhere, so skip it entirely on any other client, do not attempt to invoke or emulate it
- `review` — only when the current client is Codex; it does not exist elsewhere, so skip it entirely on any other client, do not attempt to invoke or emulate it

## Output

Present each subagent's output in full, individually, clearly separated by skill name. Do not summarize, compress, rewrite, or omit anything from any subagent's response.

After all three reports, add a **Summary** section that synthesizes the key points across all three reviews — highlight the most critical findings, group related issues, and surface any patterns. This summary is additive: it must not replace or suppress anything already reported above.
