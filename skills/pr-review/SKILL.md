---
name: pr-review
description: Perform a Pull Request review, analyzing changes from the current branch compared to its base branch.
---

## Execution

Before doing anything else, check whether the current conversation has any prior messages (i.e., messages exchanged before this skill was invoked). If there are no prior messages, run the analysis directly in this context — no subagent is needed. If there are prior messages, delegate the entire review to a subagent (via the Agent tool) without passing any current conversation context, to ensure the analysis is unbiased and not influenced by prior conversation history.

When delegating to a subagent, copy the full text of every section of this skill verbatim into the subagent prompt — do not summarize, paraphrase, or omit any section. The subagent must receive identical instructions to what is written here.

Once the subagent finishes, relay its complete output to the user exactly as returned — do not summarize, compress, or rewrite it. The subagent's response is the final output of this skill.

## Steps

1. Determine the base branch: run `gh pr view --json baseRefName -q .baseRefName` to get the base branch from the open PR. If that fails (no PR exists), fall back to `main`. Use this base branch for all diff and comparison operations throughout the review.
2. Fetch PR details and diff between the current branch and the base branch determined above.
3. Review for bugs, typos, security flaws, and performance issues.
4. Check for premature optimizations that reduce readability.
5. Look for opportunities to simplify and clarify the code.
6. Use PR description and comments as extra context about changes.
7. Identify refactoring opportunities: flag code that could be extracted, renamed, or restructured for clarity. Also search the codebase for existing patterns, utilities, or abstractions that the new code could reuse instead of reimplementing.
8. Search the full codebase for duplications: logic, structure, or patterns introduced or modified in the diff that already exist (or nearly exist) elsewhere in the project — not just within the diff itself.
9. Evaluate test quality: for each new or modified test, verify that the assertions exercise real implementation logic. Flag tests that only assert on mock behavior (e.g. verifying that a mock was called, or asserting on values the test itself injected) — these give false confidence because they test the test setup, not the code under test.

## Output instructions

- List identified issues clearly without modifying the code.
- For refactoring and duplication findings, reference the specific file and line number of the existing code in the project that is relevant.
- Use the same language as the conversation.
