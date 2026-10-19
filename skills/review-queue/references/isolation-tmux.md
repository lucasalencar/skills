# Isolation via tmux

Use this strategy when the user runs inside tmux and wants one OS-level isolated session per PR. This is the default isolation strategy for `review-queue`.

## Setup per PR

For each approved PR in order, do these steps. Stop and report when any step fails instead of silently skipping the PR.

1. **Create the worktree from that PR's own repo checkout.** Check `git worktree list` in that checkout first to reuse an existing worktree for the same branch. Otherwise fetch the PR branch per that forge's convention (pull ref, head branch, or head SHA) and create the worktree next to the checkout:
   ```sh
   git worktree add ../<repo-short-name>-pr-<number> <pr-branch-or-ref>
   ```
   `<repo-short-name>` keeps worktrees from different repos collision-free.

2. **Create the tmux window.** Only when inside tmux (`$TMUX` is set). Otherwise give the user the commands to run manually:
   ```sh
   tmux new-window -n "<repo-short-name>-pr-<number>" -c <worktree-path>
   ```
   One window per PR, named `<repo-short-name>-pr-<number>`. Never reuse a window that already runs a review.

3. **Start the review session.** In the new window, start a new session with the same agent entrypoint already in use, working directory set to the worktree. The first prompt in that session must be:
   > Invoke the skill named `branch-review`, then follow it fully for `<owner/repo>` PR #<number> (<url>) on branch `<headRefName>` against base `<baseRefName>`.

   Do not inline review instructions. Each isolated session owns its own diff, report, and follow-ups.

4. **Record the tracker entry**: repo + PR number + title, review order, worktree path, tmux window name, status (`started`).

When tmux is unavailable, fall back to printing per-PR blocks (worktree path + prompt above) so the user can open isolated sessions manually. Manually opened sessions still satisfy the isolation requirement. When even manual isolated sessions are impossible, do not review in the aggregator session: follow the mandatory-isolation rule in `SKILL.md` (explain the blocker and ask which isolation process to follow).

## Tracking

- Tracker columns for this strategy: `Repo | PR | Order | Worktree | Tmux window | Status (started / done / blocked)`.
- To check progress, read the review window output (e.g. `tmux capture-pane -p -t "<repo-short-name>-pr-<number>"`) or ask the user; never duplicate the review work.
- Cleanup is explicit: remove a worktree only after its PR is merged/closed and its session confirms it is done (run from that PR's repo checkout):
  ```sh
  git worktree remove ../<repo-short-name>-pr-<number>
  ```
