---
name: resolve-pr-comments
description: Fetch Pull Request comments and resolve them according to the suggestions.
---

## Steps

1. Fetch Pull Request comments from current branch.
2. Load the `resolve-review-comments` skill and run its triage process for
   each comment (classify intent, handle questions, evaluate and act on
   suggestions). Where that process says "reply" or "record", post it as a
   reply on the PR comment thread.
3. For comments authored by the PR owner:
   - If it is a **question**, reply with the answer to document it in the
     thread — no code change unless the answer reveals a real problem.
   - If it is a **suggestion**, just apply the change without posting a reply.
4. If a comment goes against previous definitions from a plan or chat history,
   reply explaining the reasoning instead of blindly applying.
5. When all comments are addressed, use the `commit` skill to commit and push
   the changes.

## Output instructions

- Comment text must match language used in the comment. Default is English.
