---
name: branch-review
description: Reviews branch changes by running pr-review and assess-change-impact in parallel subagents. Use when asked to review a branch, do a full review before merge, or check what a branch changes and what it might break.
---

For each skill listed below, call it in a subagent following the globally specified guidelines:

- `pr-review`
- `assess-change-impact`
- `code-review`

## Output

Present each subagent's output in full, individually, clearly separated by skill name. Do not summarize, compress, rewrite, or omit anything from either subagent's response.

After both reports, add a **Summary** section that synthesizes the key points across both reviews — highlight the most critical findings, group related issues, and surface any patterns. This summary is additive: it must not replace or suppress anything already reported above.
