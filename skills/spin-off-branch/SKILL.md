---
name: spin-off-branch
description: Extract independent work from the current branch into a new branch based on main and rebase the original on top. Use only when the user explicitly invokes this skill (e.g. "/spin-off-branch", "$spin-off-branch", "spin off branch"); never load automatically on generic branch or PR requests.
---

# Spin Off Branch

Create a small, mergeable PR branch while keeping the current branch working
on top of it. Treat this as a history rewrite of the current branch.

## Establish the split

1. Identify the target base explicitly. Default to the up-to-date `origin/main`
   when it exists; otherwise use the repository's `main`. Fetch only with the
   user's authorization when that may contact the network.
2. Inspect the branch and its commits before changing anything:

   ```sh
   git status --short
   git branch --show-current
   git log --graph --oneline --decorate <base>..HEAD
   ```

3. Require a named current branch; do not run this on `main`, `master`, or a
   detached HEAD. If the scope is not committed yet, turn it into one or more
   focused commits on the current branch before splitting it:

   ```sh
   git diff
   git diff --cached
   git add -p
   ```

   Load and follow the `commit` skill before every `git commit`. Stage only the
   spin-off scope, commit it with a focused message, then record those new
   commit IDs as the selection. If unrelated uncommitted changes remain,
   preserve them with a named stash before switching branches:

   ```sh
   git stash push -u -m "spin-off: preserve remaining work"
   ```

   Restore that stash only after the rebase completes, resolving any conflicts
   deliberately. If the user does not want to create commits, stop: Git cannot
   create a reviewable, independent branch from only part of a dirty tree
   without first recording that scope.
4. Confirm the exact commits that belong in the spin-off, the new branch name,
   and that the selected work is independently reviewable and testable. Prefer
   a contiguous set of ordinary commits. Each selected commit must be an
   ancestor of `HEAD` and must not be a merge commit.

If the scope shares an existing commit with unrelated work, first split it into
focused commits (usually with `git reset --mixed <parent>` and `git add -p`).
Load and follow the `commit` skill before recreating the commits. Explain that
this rewrites local history and inspect the result before continuing. Do not
try to extract a few hunks silently.

## Create the independent branch

Record the original branch and make a recovery ref before any rewrite:

```sh
current_branch=$(git branch --show-current)
original_tip=$(git rev-parse HEAD)
backup_branch="backup/${current_branch}-before-spin-off"
git branch "$backup_branch" "$original_tip"
```

Create the spin-off branch from the chosen base and cherry-pick the selected
commits in their original order:

```sh
git switch -c <spin-off-branch> <base>
git cherry-pick <commit-1> <commit-2> ...
```

Resolve each conflict deliberately, stage the resolution, and continue with
`git cherry-pick --continue`. To abandon the operation, use
`git cherry-pick --abort`. Run the focused tests and inspect the PR diff:

```sh
git diff --check <base>...HEAD
git diff --stat <base>...HEAD
git log --oneline <base>..HEAD
```

Do not push or create the PR unless the user asks. Make clear that this branch
is the standalone PR and should not include unrelated commits.

## Rebase the original branch onto it

Switch back to the original branch, then interactively replay its commits on
the spin-off branch:

```sh
git switch "$current_branch"
git rebase -i --rebase-merges --onto <spin-off-branch> <base>
```

In the todo list, change every commit that was cherry-picked into the spin-off
from `pick` to `drop`. Keep the remaining commits in their intended order. Do
not drop an equivalent commit by subject alone; match it to the commit IDs
selected earlier. Preserve merge structure unless the user explicitly wants to
simplify it.

Resolve conflicts, validate the resulting branch, and compare it with both
the new dependency and the saved original tip:

```sh
git diff --check <spin-off-branch>...HEAD
git log --graph --oneline --decorate <base>..HEAD
git diff --stat "$original_tip" HEAD
```

The final branch should contain the spin-off work through its new base plus
the remaining feature work. Differences from `$original_tip` should be
understood (for example, a conflict resolution), not accidental omissions.
Run the relevant tests.

If a stash was created before the split, restore it after this validation:

```sh
git stash list
git stash pop
```

Inspect the working tree and resolve any stash-application conflicts before
continuing with unrelated work.

## Recovery and remote branches

During either rebase, use `git rebase --abort` to return to the pre-rebase
state. After completing it, the backup branch remains available for inspection
or recovery. Do not delete it until the user has reviewed both branch diffs.

If the original branch was already pushed, explain that its rewritten history
requires a force-with-lease push. Ask for explicit confirmation immediately
before executing it:

```sh
git push --force-with-lease origin "$current_branch"
```

Push the new branch normally only when requested:

```sh
git push -u origin <spin-off-branch>
```
