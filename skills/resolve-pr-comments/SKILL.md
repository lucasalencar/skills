---
name: resolve-pr-comments
description: Fetch Pull Request comments and resolve them according to the suggestions.
---

## Steps

1. Before fetching comments, verify the local branch is up to date with its
   remote: `git fetch`, then check whether local HEAD is an ancestor of the
   remote HEAD (`git merge-base --is-ancestor HEAD @{u}`).
   - If local HEAD is an ancestor of remote HEAD (no unpushed local commits)
     and the working tree is clean, fast-forward automatically
     (`git merge --ff-only`) — this only moves the branch pointer, no commit
     is rewritten, so there's nothing to lose.
   - Otherwise — local has unpushed commits, the remote history was rewritten
     (force-push/rebase/amend, so local HEAD is no longer an ancestor), or the
     working tree has uncommitted changes — ask the user before rebasing.
     Don't rebase without confirmation in these cases, since replaying local
     commits on top of diverged/rewritten history risks conflicts and lost
     work.
2. Fetch Pull Request comments from current branch.
3. Load the `resolve-review-comments` skill and run its triage process for
   each comment (classify intent, handle questions, evaluate and act on
   suggestions). Where that process says "reply" or "record", post it as a
   reply on the PR comment thread.
4. For comments authored by the PR owner:
   - If it is a **question**, reply with the answer to document it in the
     thread — no code change unless the answer reveals a real problem.
   - If it is a **suggestion**, just apply the change without posting a reply.
5. If a comment goes against previous definitions from a plan or chat history,
   reply explaining the reasoning instead of blindly applying.
6. When all comments are addressed, use the `commit` skill to commit and push
   the changes.

## Output instructions

- Comment text must match language used in the comment. Default is English.
- Keep replies concise: answer the specific question or point raised, nothing more. Only reference a file or code snippet when it's actually needed to make the answer clear — skip it otherwise.
- Append a short signature at the end of each posted reply disclosing it was AI-generated, naming the client in use (e.g. Claude Code, Codex) with the model in parentheses (e.g. "— reply generated with <client> (<model name>)").
