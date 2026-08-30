---
name: resolve-pr-comments
description: Fetch and resolve Pull Request review comments. Use whenever the user wants to address PR feedback — triggers include "resolver comentários do PR", "endereçar comentários", "resolver feedback do PR", "resolve PR comments", "address review comments", "corrigir o que foi comentado no PR", or wants to apply suggestions from a code review.
---

## Steps

1. Load and follow `pr-comment-writing` before drafting or posting any reply. Apply its **Replies** and **Language** instructions.
2. Before fetching comments, verify the local branch is up to date with its
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
3. Fetch Pull Request comments from current branch.
4. Load the `resolve-review-comments` skill and run its triage process for
   each comment (classify intent, handle questions, evaluate and act on
   suggestions). Where that process says "reply" or "record", post it as a
   reply on the PR comment thread.
5. For comments authored by the PR owner:
   - If it is a **question**, reply with the answer to document it in the
     thread — no code change unless the answer reveals a real problem.
   - If it is a **suggestion**, just apply the change without posting a reply.
6. If a comment goes against previous definitions from a plan or chat history,
   reply explaining the reasoning instead of blindly applying.
7. When all comments are addressed, use the `commit` skill to commit and push
   the changes.
