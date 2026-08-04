---
name: iterative-implementation
description: Coordinate Jira tasks as small, dependency-ordered implementation iterations, with one subagent, worktree, branch, and pull request per task. Use for iterative or dependency-ordered delivery across tickets. Require each task's ID, title, scope, acceptance criteria, and dependencies; resolve missing details before dispatch.
---

# Iterative implementation

Treat the task map as a dependency graph. Coordinate the work; never implement a task in the coordinator checkout.

## Invariants

- Use the Jira ID as each task's primary identifier in prompts, branches, worktrees, and reports. Add a PR number only for navigation.
- Give each task one dedicated subagent, isolated worktree, branch, and PR.
- Keep implementation, validation, commits, and PR scope task-specific. Never combine tasks, even when small.
- Dispatch only tasks whose required fields and branch/PR bases are known and that have no unresolved blocker.

## Workflow

1. Validate every task's ID, title, scope, acceptance criteria, and dependencies. Report cycles and unknown dependency IDs; ask whether unknown dependencies are valid and already complete. Block only affected tasks and present the rest of the graph.
2. Render the complete dependency tree and compute the ready set from the table below. Identify tasks that can run in parallel and recommend completing the current ready set before newly unblocked work.
3. Dispatch the user-authorized ready tasks with the contract below. If the user authorized consecutive iterations, continue as tasks become ready; otherwise stop after the current ready set.
4. After each status change, verify PR state, synchronize Jira, regenerate the tree, and recompute the ready set.
5. After each iteration, report task branches and PRs, validation, newly ready tasks, and blockers.

## Branch and PR bases

Determine both bases before dispatch:

| Dependency state | Branch base | PR base | Ready? |
| --- | --- | --- | --- |
| None | `main` | `main` | Yes |
| One, with an unmerged PR | Dependency branch | Dependency branch | Yes |
| One, merged | `main` | `main` | Yes |
| Multiple, any unmerged | — | — | No |
| Multiple, all merged | `main` | `main` | Yes |

When a stacked PR's base merges, retarget the child PR to `main` and verify that its diff contains only the child's work. Start a task with multiple dependencies only after all are merged into `main`; report which prerequisites must merge.

## Subagent dispatch contract

Send a complete task-specific prompt:

```text
Task: PROJ-123 — <title>
Scope and acceptance criteria: <task-specific scope>
Dependencies: <direct Jira IDs, branches/PRs, and merge state>
Branch base: <branch>
PR base: <branch>

Before coding:
- Move the Jira card to the project's equivalent of In Progress and assign it to the requesting user. Update a parent only when the project's workflow or aggregation rule requires it.
- Create an isolated worktree from the branch base. Do not edit the coordinator checkout or another task's worktree.

Implementation:
- Invoke implement-plan and continue until complete or externally blocked.
- Keep all edits, commits, validation, and the PR limited to this task.
- Open one PR with open-pr, targeting the PR base.

Report back:
- Jira status, worktree path, branch, PR URL and state, validation and results, and blockers.
```

## Dependency tree

For dependent tasks or more than two tasks, use box-drawing characters (`├──`, `└──`, `│`). Start each full node with its status, Jira ID, and title; add its PR number when one exists. Nest a task under its first declared dependency. For additional dependencies, append `also depends on: <IDs>` to the full node and place `↳ <ID>` under each additional dependency. Never duplicate the full node.

Statuses: `⚪ not started`, `📝 draft`, `🚧 in progress`, `👀 in review`, `✅ done`.

```text
Dependency tree

├── ✅ PROJ-124 — Design token schema
│   ├── 🚧 PROJ-125 — Implement token service (PR #482)
│   │   └── ⚪ PROJ-126 — Write migration script
│   └── ⚪ PROJ-123 — Auth migration (also depends on: PROJ-127)
└── 👀 PROJ-127 — Update client SDK (PR #484)
    └── ↳ PROJ-123

Ready now: PROJ-126
```

Regenerate the tree instead of describing deltas. Use only Jira and PR IDs verified directly or reported by the responsible subagent.

## Jira synchronization

First map the project's workflow states equivalent to In Progress, In Review, and Done. If a mapping is unknown, report it and do not transition the card.

| Evidence | Jira state |
| --- | --- |
| Work started, branch pushed, or draft PR open | In Progress |
| PR ready for review | In Review |
| PR merged and no deployment gate applies, or deployment confirmed | Done |

Synchronize Jira whenever gathering status, using the verified PR state or direct subagent evidence. Skip no-op transitions. If a required deployment is unconfirmed, do not mark the task Done; report the blocker. Update a parent only from direct evidence or its documented aggregation rule.
