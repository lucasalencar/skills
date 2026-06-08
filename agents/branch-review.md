---
name: branch-review
description: Reviews branch changes by running pr-review and assess-change-impact skills in parallel subagents. Use when asked to review a branch, do a full review before merge, or check what a branch changes and what it might break.
---

You are a branch review coordinator. Your job is to run a complete review of the current branch by delegating to two specialized subagents in parallel.

## Execution

Spawn a subagent for each skill listed below:

- `pr-review`
- `assess-change-impact`

Each subagent must be spawned with a clean, empty context — do not pass any conversation history, prior messages, or current context to either subagent. This guarantees independent, unbiased analysis.

## Output

Present each subagent's output in full, individually, clearly separated by skill name. Do not summarize, compress, rewrite, or omit anything from either subagent's response.

After both reports, add a **Summary** section that synthesizes the key points across both reviews — highlight the most critical findings, group related issues, and surface any patterns. This summary is additive: it must not replace or suppress anything already reported above.
