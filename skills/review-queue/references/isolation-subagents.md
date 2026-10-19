# Isolation via subagents

Use this strategy when the user prefers reviews orchestrated inside the current session (no tmux windows) and the client supports parallel subagents with independent context. Each PR still gets its own worktree and its own subagent; the aggregator session never inspects diffs itself. Results return to the aggregator through subagent reports.

## Setup per PR

For each approved PR in order, do these steps. Stop and report when any step fails instead of silently skipping the PR.

1. **Create the worktree from that PR's own repo checkout.** Check `git worktree list` in that checkout first to reuse an existing worktree for the same branch. Otherwise fetch the PR branch per that forge's convention (pull ref, head branch, or head SHA) and create the worktree next to the checkout:
   ```sh
   git worktree add ../<repo-short-name>-pr-<number> <pr-branch-or-ref>
   ```
   Resolve the worktree to an absolute path — the subagent prompt needs it, since subagents cannot inherit the aggregator's working directory. `<repo-short-name>` keeps worktrees from different repos collision-free.

2. **Spawn one subagent per PR.** One subagent per PR, never one subagent for several PRs and never two subagents sharing a worktree. Dispatch approved PRs in parallel up to the agreed batch size (default 3–5); queue the rest. The subagent prompt must contain, in order:
   - Repo (`<owner/repo>`), PR number, PR URL, head branch, base branch.
   - Absolute worktree path and instruction to do all file reads and commands from there (e.g. `git -C <worktree> ...`, read `<worktree>/path/to/file`), never from the aggregator checkout.
   - Instruction to invoke the skill named `branch-review`, then follow it fully for that PR and range.
   - The subagent output contract below.

3. **Record the tracker entry**: repo + PR number + title, review order, worktree path, subagent id, status (`spawned`).

Do not inline review instructions in place of `branch-review`. Do not let the subagent modify code, switch branches, or touch worktrees belonging to other PRs.

## Subagent output contract

Every review subagent returns exactly this to the aggregator — full detail lives in its worktree report, the message back is a handoff, not a rewrite:

- Status: `done` or `blocked` (plus the blocker and what was attempted).
- Worktree path and full `.reviews/<iteration>.md` report path inside that worktree.
- Verbatim `branch-review` summary sections (`In-scope issues` / `Out-of-scope issues`, or `No actionable findings`), with `BR-NNN` identifiers kept per PR (prefix with repo + PR number when aggregating so identifiers never collide).
- Per-finding location as worktree-relative `path:line` plus the PR URL it belongs to.

When a subagent reports `blocked` (fetch failed, base unresolvable, history ambiguous), keep its worktree, mark the tracker `blocked`, and surface the exact question it needs answered. Never work around a blocked review by inspecting the diff in the aggregator session.

## Aggregation and tracking

- Tracker columns for this strategy: `Repo | PR | Order | Worktree | Subagent | Status (spawned / done / blocked)`.
- The aggregator synthesizes; it does not re-review. Group returned findings per PR under a `owner/repo#number` heading, preserve locations and impacts, and link each group to its worktree report path. Findings from different PRs are independent — do not deduplicate across PRs.
- If two subagents report on the same underlying problem within one PR (e.g. dimension overlap), merge them into one finding keeping all distinct impacts, following `branch-review` synthesis rules.
- Report completion per PR only from what its own subagent returned.
- Cleanup is explicit: remove a worktree only after its PR is merged/closed and its review is handed off:
  ```sh
  git -C <repo-checkout> worktree remove ../<repo-short-name>-pr-<number>
  ```
