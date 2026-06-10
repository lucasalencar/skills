---
name: resolve-pr-comments
description: Fetch Pull Request comments and resolve them according to the suggestions.
---

## Steps

1. Fetch Pull Request comments from current branch.
2. For each comment, first determine its intent:
   - **Question**: the reviewer is asking something (about design, behavior,
     naming, intent, etc.) — not necessarily requesting a change.
   - **Suggestion**: the reviewer is proposing a concrete code change.
   - **Mixed**: both a question and an implicit suggestion.

3. For **questions**:
   - Explore the code, context, and conversation history to try to answer it.
   - If the answer is clear from the code, reply with the explanation — no code
     change needed unless the answer reveals a real problem.
   - If the question cannot be fully answered from available context, bring it
     to the user before doing anything else. Only proceed with a change after
     the question is resolved and it's clear a change is warranted.

4. For **suggestions**, perform a technical evaluation before acting:
   - Read the actual code at the relevant location.
   - Assess whether the suggestion is correct, necessary, and beneficial given
     the current implementation — not just based on LLM judgment.
   - If the suggestion conflicts with previous decisions in the conversation
     history, plan, or codebase patterns, factor that in.
   - Classify and act:
     - **Apply automatically**: clearly correct and confirmed by the code (e.g.
       obvious bugs, simple improvements, clear style fixes). Apply without
       asking.
     - **Apply with note**: sound but involves trade-offs worth surfacing —
       apply and note the reasoning in the reply.
     - **Ask the user**: ambiguous, has significant downsides, or cannot be
       fully evaluated from the code alone. Pause and ask before proceeding.

5. For comments authored by the PR owner:
   - If it is a **question**, reply with the answer to document it in the
     thread — no code change unless the answer reveals a real problem.
   - If it is a **suggestion**, just apply the change without posting a reply.
6. If a comment goes against previous definitions from a plan or chat history,
   reply explaining the reasoning instead of blindly applying.
7. When all comments are addressed, commit and push changes.

## Output instructions

- Comment text must match language used in the comment. Default is English.
