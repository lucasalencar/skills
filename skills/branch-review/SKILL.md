---
name: branch-review
description: Reviews branch changes by running pr-review and assess-change-impact in parallel subagents. Use when asked to review a branch, do a full review before merge, or check what a branch changes and what it might break.
---

## Execution

Spawn two subagents in parallel via the Agent tool. Each subagent must receive a clean, empty context — do not pass any conversation history, prior messages, or current context.

For each subagent, instruct it to:
1. Read the corresponding skill file listed below
2. Follow the instructions in that file directly — **skip any section that says to delegate to a subagent**, since it is already running as one

### Subagent 1: PR Review

Skill file: `~/.claude/skills/pr-review/SKILL.md`

### Subagent 2: Change Impact Analysis

Skill file: `~/.claude/skills/assess-change-impact/SKILL.md`

---

## Output

Present each subagent's output in full, individually, clearly separated by skill name. Do not summarize, compress, rewrite, or omit anything from either subagent's response.

After both reports, add a **Summary** section that synthesizes the key points across both reviews — highlight the most critical findings, group related issues, and surface any patterns. This summary is additive: it must not replace or suppress anything already reported above.
