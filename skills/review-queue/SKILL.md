---
name: review-queue
description: Review multiple open pull requests from one or more repos in parallel with prioritization and isolated sessions. Use whenever the user wants to review several PRs, batch review, review queue, triage open PRs, or run branch reviews in parallel.
---

# Review Queue

Coordinate batch review of open PRs across one or more repos. Default scope is the current repo (where this session runs) when the user names no repos. When the user names multiple repos, cover all of them. This session acts only as the aggregator: it lists PRs, agrees on a review order, spawns one isolated review per PR, and tracks progress. It never reviews code itself.

Isolation is mandatory, not a preference. Every `branch-review` must run in its own isolated session with its own worktree. Never run `branch-review`, its dimension subagents, or any diff inspection for a queued PR inside this aggregator session — not directly, not via subagents, not as a shortcut for "just one quick PR". This session lists, orders, spawns, and tracks; it never reviews.

Isolation model per PR: each PR is reviewed in an isolated session defined by the active isolation strategy. Two strategies exist: tmux (see `references/isolation-tmux.md`, the default) and subagents (see `references/isolation-subagents.md`). Every strategy follows the same contract: one worktree per PR, one independent session running the `branch-review` skill, and one tracker entry. Confirm the strategy with the user when it is ambiguous; otherwise use tmux.

When no isolation strategy can be applied (e.g. no supported session mechanism is available and the user cannot open new sessions, worktree creation fails and has no safe alternative), stop before spawning anything. Explain exactly which requirement failed, what was attempted, and why running the review in this session is not an acceptable fallback. Then ask the user which isolation process to follow (fix the blocker, switch strategy, provide manual session commands, or abort). Do not degrade to in-session review on your own authority.

## 1. Resolve scope and access method, then fetch open PRs

Resolve scope first: when the user named repos (e.g. `owner/a`, `owner/b`), use exactly those. Otherwise default to the current repo — resolve it from the session directory with whatever repo tooling the environment provides and confirm it with the user when ambiguous.

Detect the environment before touching any PR data. The skill never hardcodes how PRs are fetched — the agent already knows the available tools, so let it decide. Check in this order and use the first capable option: (1) PR operations exposed as MCP resources/tools in this session, (2) a forge CLI available on `PATH` (or whatever the repo already uses — verify with `command -v`), (3) the forge's API directly. When nothing is available, stop and ask the user which access method to use instead of guessing commands.

For each repo, fetch its open PRs with at least: PR number, title, author, size signal (added/removed lines or equivalent), labels, created and updated timestamps, head and base branches, draft state, and URL. Tag every PR with its repo.

Forge notes: keep repo-qualified identity (`<owner/repo>#<number>`) everywhere since PR numbers collide across repos; exclude drafts by default; fetch each PR's branch per that forge's convention (e.g. pull ref or head branch/SHA) when creating its worktree.

Also resolve each repo's local checkout path: the session directory for the default repo, and for any additional repo either an existing local checkout or a path the user provides. Worktrees and review sessions are always created from that repo's own checkout — never mix branches across repos.

- Exclude drafts by default; include them only when the user asks.
- When the list is empty, stop and say so.
- When a single PR needs more signal (labels, linked issues), fetch its detail through the same access method.
- End this step by writing the full table into chat — one row per open PR with columns: repo, number, title, author, size, age, labels, head branch. Keep repo-qualified identity (`<owner/repo>#<number>`) everywhere, since PR numbers collide across repos. This step is not done while the data exists only in tool output. Never ask the strategy question (step 2) before this table is visible in chat.

## 2. Show the data, then propose a prioritization strategy

First verify the full PR table from step 1 is visible in chat immediately above the proposals. If it is not visible — it was never rendered, only fetched — render it now (same columns as step 1) before proposing anything. Then add a one-line read of the landscape below the table (e.g. "5 PRs, 2 under 100 lines, 1 with `priority:high`, oldest open 21 days"), so the strategy choice is grounded in data, not memory.

Then derive at least two concrete suggestions from that data. Always consider these three, plus author grouping when relevant:

- **Quick wins first**: sort by size (added + removed lines or the forge's equivalent) ascending. Best when the goal is to unblock many small PRs fast.
- **Team priority first**: labels indicating priority/bug/customer impact, linked issues, requested-changes state, or explicitly requested by the user. Best when impact matters more than size.
- **Oldest first**: sort by `createdAt` (or `updatedAt` for stale PRs) ascending. Best when PRs are rotting or blocking others.

Then go beyond this list: inspect the actual PR data and propose any other strategy the data supports that could beat the defaults — for example riskiest-first (large diffs, many files, migration/schema/auth touchpoints), most-blocked-first (stacked PRs others depend on, merge conflicts, failing checks), author's own PRs last (to avoid self-review bias), or reviewer-load balancing (group by author or area so parallel sessions don't collide). Only suggest one when the data genuinely backs it; never invent a strategy to fill space.

Mark exactly one strategy as **Recommended**, with a one-sentence reason tied to the table (e.g. "Recommended: quick wins first — 3 of 5 PRs are under 150 lines and unblock the release"). When no strategy clearly wins, say so and name the tiebreak you applied.

State which PRs each suggested order would put first (e.g. "#12, #34 are <200 lines" vs "#45 has `priority:high` label"). Then ask the user to pick one strategy, combine them (e.g. high-priority first, ties broken by size), filter by author, or supply a manual order. Do not proceed to step 3 without an explicit order.

## 3. Confirm the review order and batch size

Record the final ordered list of repo-qualified PRs (e.g. `owner/a#12 → owner/b#45 → owner/a#34`). Then confirm:

- The exact order.
- How many to start now when the list is long (default: start at most 3–5 in parallel, queue the rest).
- Worktree location convention per repo (default: sibling directory `../<repo-short-name>-pr-<number>` next to that repo's checkout; keep it consistent and collision-free across repos).
- Isolation strategy: tmux (default) or subagents.

Do not start more sessions than the user approved.

## 4. Spawn one isolated review per PR

Load the active isolation strategy reference before spawning anything — `references/isolation-tmux.md` by default, `references/isolation-subagents.md` when the user chose subagents — and follow it fully for worktree setup, session creation, progress checks, result handoff, and cleanup.

Every strategy must satisfy this contract:

1. One worktree per PR, created from that PR's own repo checkout (reuse when `git worktree list` in that checkout already has the branch). Worktree directory names must include the repo short name so PRs from different repos never collide.
2. One independent session per PR whose first instruction invokes the `branch-review` skill with repo, PR number, URL, head branch, and base branch. Session names must include the repo, following the active strategy's naming.
3. One tracker entry per PR with at least: repo + PR number + title, review order, session location, status (`started`).

Prohibited: running any PR review in this session, sharing one worktree/session across two PRs, or letting the aggregator inspect diffs to "fill in" for a missing session. A subagent counts as isolated only under the subagents strategy (own worktree, own session context, results returned via the output contract) — never as an ad-hoc helper inside the tmux strategy.

Stop and report when any PR fails to spawn instead of silently skipping it. Do not start more sessions than the user approved. When isolation is impossible, follow the mandatory-isolation rule above: explain the blocker and ask which isolation process to follow.

## 5. Track as aggregator

Keep this session as the overview. Do not fetch diffs or report findings here.

- Maintain one tracker table and update it when sessions are created, finish, or fail. Column layout comes from the active isolation strategy.
- To check progress, use the strategy's progress mechanism or ask the user; never duplicate the review work.
- Report completion per PR only based on what its own session produced.
- Cleanup follows the strategy (only after its PR is merged/closed and its session confirms it is done).

## Output

- The scope (repos covered), the access method used (MCP vs CLI vs API), and the fetched PR table with the data that drove the suggestions.
- The chosen strategy and final review order.
- The tracker table with worktree path and session location per started PR, plus how to attach to each session.
- Any PRs left queued (not started) and what starts them.
- The active isolation strategy (`references/isolation-tmux.md` by default, `references/isolation-subagents.md` when chosen).
