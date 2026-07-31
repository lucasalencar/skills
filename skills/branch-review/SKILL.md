---
name: branch-review
description: Reviews branch changes by running a PR review across multiple dimensions plus impact analysis, each in parallel subagents. Use when asked to review a branch, do a full review before merge, or check what a branch changes and what it might break.
---

Determine the base branch once: run `gh pr view --json baseRefName -q .baseRefName`. If that fails, fall back to `main`. Pass the resolved base branch to every subagent below — each subagent fetches the diff, description, and comments itself during its own session rather than receiving them pasted into its prompt, so it can re-fetch, re-diff, or drill into specific files as needed instead of being limited to a snapshot taken up front.

Call every applicable item below, each in its own subagent, following the globally specified guidelines. This applies identically on every invocation of this skill — first call or the tenth in a row within a loop: never skip, merge, or substitute any applicable one. Re-read this file fresh on every invocation before dispatching subagents — do not rely on what you recall doing in a previous iteration within this same conversation. A previous iteration's subagent prompts are not a template to reuse or abbreviate; rebuild every subagent prompt from this file and its reference files from scratch, every time.

## Independent skills

Each bullet is the name of an actual skill. The subagent prompt for each one must explicitly instruct the subagent to load and follow that skill (e.g. "Invoke the skill named `assess-change-impact`, then follow it fully") — never paraphrase or reconstruct the skill's behavior from memory instead of loading it, and never omit this instruction because a prior iteration already included it.

- `assess-change-impact` — always
- `code-review` — only when the current client is Claude Code; it does not exist elsewhere, so skip it entirely on any other client, do not attempt to invoke or emulate it
- `review` — only when the current client is Codex; it does not exist elsewhere, so skip it entirely on any other client, do not attempt to invoke or emulate it

## PR review dimensions

Spawn one subagent per file below. Before building each subagent's prompt, use the Read tool to load that reference file's current contents — do not paste from memory, even if you read it earlier in this conversation or in a previous loop iteration. Each subagent's prompt must contain, in this order: the resolved base branch (with an instruction to fetch the diff, description, and comments itself against that base branch), the reference file's content copied verbatim and in full (do not summarize, paraphrase, trim, or omit any part of it), and the **Output instructions** section further down.

- `references/correctness.md` — always
- `references/security.md` — always
- `references/performance.md` — always
- `references/readability.md` — always
- `references/maintainability.md` — always
- `references/reuse-duplication.md` — always
- `references/test-quality.md` — always

## Output instructions (for each dimension subagent)

- List identified issues clearly without modifying the code.
- For refactoring and duplication findings, reference the specific file and line number of the existing code in the project that is relevant.
- Use the same language as the conversation.

## Output

Present each subagent's output in full, individually, clearly separated by name (skill name or dimension name). Do not summarize, compress, rewrite, or omit anything from any subagent's response.

After all reports, add a **Summary** section that synthesizes the key points across all of them — highlight the most critical findings, group related issues, and surface any patterns. This summary is additive: it must not replace or suppress anything already reported above.
