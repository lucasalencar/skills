---
name: branch-review
description: Review a branch, PR, or recent commits across multiple dimensions (correctness, security, performance, etc.) plus impact analysis in parallel subagents. Use whenever the user wants a code review — triggers include "revisar branch", "revisar PR", "review branch", "review PR", "revisar código", "revisar mudanças", "code review", "revisa meu PR", "check what this change might break", or wants a full review before merge.
---

Resolve one review range before dispatching subagents:

1. Honor an explicit commit range or fixed point from the user.
2. Otherwise, run `gh pr view --json baseRefName -q .baseRefName`. When it succeeds, review `<base>...HEAD`.
3. When no PR exists, resolve the base branch as `main`. If `HEAD` is ahead of `main`, review `main...HEAD`.
4. When `HEAD` is on `main`, or it has no commits beyond `main`, infer a coherent recent commit set from history. Inspect recent commits with their dates, authors, messages, changed paths, and diff stats. Starting at `HEAD`, walk backward and include contiguous commits that appear to belong to the same unit of work. Treat overlap in files, directories, symbols, or feature area; a shared commit-message theme; the same author; and temporal proximity as supporting evidence. Stop before a merge, a clear shift in feature area or intent, a different author unless the history supports collaboration on the same change, or a substantial time gap. Prefer semantic cohesion over a fixed commit count. Use `<oldest-selected-commit>^..HEAD` as the review range.

Before dispatching, send a progress update with the selected range and a one-sentence rationale. If the history does not support a defensible boundary, ask the user for the starting commit instead of choosing an arbitrary count.

Every subagent receives the resolved range and fetches the diff itself. When a PR exists, it also fetches its description and comments in its own session.

On every invocation, reread this skill and reconstruct every prompt from it and the current reference files. Call each applicable item once in its own subagent. Build all prompts, then dispatch every subagent from both sections in one parallel batch.

## Subagent output contract

Include this contract in every subagent prompt, after any skill-specific or dimension-specific instructions:

- Do not modify code.
- Report only actionable findings supported by the reviewed code. For each finding, cite the relevant `path:line`; for a cross-cutting finding without a single location, cite all relevant locations.
- Give a concise explanation and at least one concrete, non-speculative impact for each finding.
- Use the same language as the conversation.
- When no actionable findings exist, state `No actionable findings.`

## Independent skills

Each bullet is the name of an actual skill. Its subagent prompt must explicitly instruct the subagent to load and follow that skill (for example, "Invoke the skill named `assess-change-impact`, then follow it fully").

- `assess-change-impact` — always
- `code-review` — only when the current client is Claude Code; it does not exist elsewhere, so skip it entirely on any other client, do not attempt to invoke or emulate it
- `review` — invoke when the current client is Codex. Also invoke it when the current client is Claude Code and the Codex plugin is installed: dispatch the review to Codex through that plugin. On any other client, or when that plugin is unavailable, skip it entirely; do not attempt to invoke or emulate it.

## Change review dimensions

Spawn one subagent per file below. Load each reference file's current contents before building its prompt. The prompt must contain, in order: the resolved range and instruction to fetch the review materials; the reference file copied verbatim and in full; then the **Subagent output contract**.

- `references/correctness.md` — always
- `references/security.md` — always
- `references/performance.md` — always
- `references/readability.md` — always
- `references/maintainability.md` — always
- `references/reuse-duplication.md` — always
- `references/test-quality.md` — always

## Output

Write all subagent outputs to one report, `.reviews/<iteration>.md`. When called by `branch-review-loop`, use its 1-based loop number as `<iteration>`; otherwise, use a timestamp. Create the directory as needed. Give every subagent its own clearly labeled Markdown section, using the skill or dimension name as the section title. Copy each output in full and verbatim into its section: do not summarize, compress, rewrite, or omit anything.

In the final chat response, return only a **Summary** section that synthesizes the identified issues across all subagents. Merge duplicate reports of the same underlying problem into one finding, retaining all relevant impacts. Report a finding only when it has a concrete, non-speculative impact.

```markdown
### BR-001 — Title

**Location:** `path/to/file:line`

**Finding:** A concise statement of the problem.

**Explanation:** One short paragraph explaining what is wrong, where it occurs, and why it matters. Give enough context for a reader to understand the finding without opening the full reports; do not reproduce the full investigation.

**Impact:**
- Concrete consequence 1.
- Concrete consequence 2, when applicable.
```

Each finding needs one or more impact bullets. Use a unique, sequential identifier (`BR-001`, `BR-002`, and so on) wherever that finding appears in the summary. If there are no findings, write `No actionable findings.` After the findings, include the path to the full report document.
