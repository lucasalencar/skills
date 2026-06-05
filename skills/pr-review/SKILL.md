---
name: pr-review
description: Perform a Pull Request review, analyzing changes from the current branch compared to main.
---

## Execution

Always delegate the entire review to a subagent (via the Agent tool) without passing any current conversation context. This guarantees the analysis is unbiased and not influenced by prior conversation history.

When building the subagent prompt, copy the full text of every section of this skill verbatim — do not summarize, paraphrase, or omit any section. The subagent must receive identical instructions to what is written here.

Once the subagent finishes, relay its complete output to the user exactly as returned — do not summarize, compress, or rewrite it. The subagent's response is the final output of this skill.

## Steps

1. Fetch PR details and diff between the current branch and main.
2. Review for bugs, typos, security flaws, and performance issues.
3. Check for premature optimizations that reduce readability.
4. Look for opportunities to simplify and clarify the code.
5. Use PR description and comments as extra context about changes.

## Output instructions

- List identified issues clearly without modifying the code.
- Use the same language as the conversation.
