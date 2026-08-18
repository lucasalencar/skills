---
name: branch-review
description: Reviews a branch or a coherent set of recent commits by running a change review across multiple dimensions plus impact analysis, each in parallel subagents. Use when asked to review a branch, review recent work committed directly to the base branch, do a full review before merge, or check what a change set might break.
---

Resolve one review range before dispatching subagents:

1. Honor an explicit commit range or fixed point from the user.
2. Otherwise, run `gh pr view --json baseRefName -q .baseRefName`. When it succeeds, review `<base>...HEAD`.
3. When no PR exists, resolve the base branch as `main`. If `HEAD` is ahead of `main`, review `main...HEAD`.
4. When `HEAD` is on `main`, or it has no commits beyond `main`, infer a coherent recent commit set from history. Inspect recent commits with their dates, authors, messages, changed paths, and diff stats. Starting at `HEAD`, walk backward and include contiguous commits that appear to belong to the same unit of work. Treat overlap in files, directories, symbols, or feature area; a shared commit-message theme; the same author; and temporal proximity as supporting evidence. Stop before a merge, a clear shift in feature area or intent, a different author unless the history supports collaboration on the same change, or a substantial time gap. Prefer semantic cohesion over a fixed commit count. Use `<oldest-selected-commit>^..HEAD` as the review range.

State the selected range and a one-sentence rationale before dispatch. If the history does not support a defensible boundary, ask the user for the starting commit instead of choosing an arbitrary count.

Pass the resolved review range to every subagent below. Each subagent fetches the diff and, when a PR exists, its description and comments during its own session rather than receiving them pasted into its prompt, so it can re-fetch, re-diff, or drill into specific files as needed instead of being limited to a snapshot taken up front.

Call every applicable item below, each in its own subagent, following the globally specified guidelines. This applies identically on every invocation of this skill — first call or the tenth in a row within a loop: never skip, merge, or substitute any applicable one. Re-read this file fresh on every invocation before dispatching subagents — do not rely on what you recall doing in a previous iteration within this same conversation. A previous iteration's subagent prompts are not a template to reuse or abbreviate; rebuild every subagent prompt from this file and its reference files from scratch, every time.

Dispatch every subagent from both sections below — independent skills and PR review dimensions — together, in a single batch of parallel tool calls. Do not wait for the independent skills to finish before starting the dimension subagents, and do not stagger them into separate rounds for any other reason: build every prompt first, then launch all of them at once.

## Independent skills

Each bullet is the name of an actual skill. The subagent prompt for each one must explicitly instruct the subagent to load and follow that skill (e.g. "Invoke the skill named `assess-change-impact`, then follow it fully") — never paraphrase or reconstruct the skill's behavior from memory instead of loading it, and never omit this instruction because a prior iteration already included it.

- `assess-change-impact` — always
- `code-review` — only when the current client is Claude Code; it does not exist elsewhere, so skip it entirely on any other client, do not attempt to invoke or emulate it
- `review` — invoke when the current client is Codex. Also invoke it when the current client is Claude Code and the Codex plugin is installed: dispatch the review to Codex through that plugin. On any other client, or when that plugin is unavailable, skip it entirely; do not attempt to invoke or emulate it.

## Change review dimensions

Spawn one subagent per file below. Before building each subagent's prompt, use the Read tool to load that reference file's current contents — do not paste from memory, even if you read it earlier in this conversation or in a previous loop iteration. Each subagent's prompt must contain, in this order: the resolved review range (with an instruction to fetch that diff itself and, when a PR exists, fetch its description and comments), the reference file's content copied verbatim and in full (do not summarize, paraphrase, trim, or omit any part of it), and the **Output instructions** section further down.

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

Write each subagent's output to `.reviews/<iteration>/<subagent-name>.md`, using the skill or dimension name for `<subagent-name>` (for example, `.reviews/1/assess-change-impact.md` or `.reviews/1/correctness.md`). When called by `branch-review-loop`, use its 1-based loop number as `<iteration>`; otherwise, use a timestamp. Create the directory as needed. Copy that subagent's output in full, verbatim: do not summarize, compress, rewrite, or omit anything.

In the chat response, return only a **Summary** section that synthesizes the identified issues across all subagents — highlight the most critical findings, group related issues, and surface any patterns. Present every distinct finding as `BR-001 — Title`, followed by a concise one- or two-sentence description of the problem and its relevant consequence. Use a unique, sequential identifier (`BR-001`, `BR-002`, and so on) and include it wherever that finding appears in the summary. Include the paths to the full report documents.
