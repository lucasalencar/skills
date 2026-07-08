---
name: resolve-hunk-comments
description: Fetch the review comments the user left in a live Hunk session and address them in the current code. Use when the user asks to resolve, address, or act on comments they added while reviewing a diff in Hunk (e.g. "resolve my hunk comments", "endereça os comentários que eu fiz no hunk").
---

## Steps

1. Load the `hunk-review` skill for the CLI conventions (session selection, navigate, comment commands).
2. List the user's own comments: `hunk session comment list --repo . --type user --json`.
   - If there are none, tell the user and stop.
3. For each comment, navigate to it (`hunk session navigate --repo . --file <path> --new-line <n>` or `--old-line <n>`) and read the surrounding code to understand context, then determine intent:
   - **Question**: the user is asking something (about design, behavior, naming, intent) — not necessarily requesting a change.
   - **Suggestion**: the user is proposing a concrete code change.
   - **Mixed**: both a question and an implicit suggestion.
4. For **questions**:
   - Explore the code and conversation history to try to answer it.
   - If the answer is clear, note it for the summary — no code change unless the answer reveals a real problem.
   - If it can't be answered from available context, bring it to the user before doing anything else.
5. For **suggestions**, perform a technical evaluation before acting:
   - Read the actual code at the relevant location.
   - Assess whether the suggestion is correct, necessary, and beneficial given the current implementation.
   - If it conflicts with previous decisions in the conversation, plan, or codebase patterns, factor that in.
   - Classify and act:
     - **Apply automatically**: clearly correct and confirmed by the code.
     - **Apply with note**: sound but involves trade-offs worth surfacing in the summary.
     - **Ask the user**: ambiguous, has significant downsides, or can't be fully evaluated from the code alone.
6. Do not remove or clear comments from the session (`comment rm`/`comment clear`) — leave that to the user, since the comments are their own review notes.
7. Do not commit changes automatically. If the user wants to commit afterward, use the `commit` skill.

## Output

When all comments are addressed, summarize per comment: what it asked/suggested, what was done (applied / applied with note / needs input), and file:line reference.
