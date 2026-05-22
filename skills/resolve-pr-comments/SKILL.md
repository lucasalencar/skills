---
name: resolve-pr-comments
description: Fetch Pull Request comments and resolve them according to the suggestions.
---

## Steps

1. Fetch Pull Request comments from current branch.
2. Read and act on all comments that contain suggestions, including those
   authored by the PR owner (the current user). However, do NOT post replies
   on GitHub to comments authored by the PR owner — just apply the change.
3. If there are any comments that goes against some previous definitions
   from a plan or chat history, consider answering it with the reasoning.
4. If the comment is sound, proceed with adjusting the code.
5. When all comments are addressed, commit and push changes.

## Output instructions

- Comment text must match language used in the comment. Default is English.
