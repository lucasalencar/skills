---
name: iterative-implementation
description: Plan and deliver a task map as small, dependency-ordered implementation iterations. Use when the user requests iterative implementation to turn a dependency tree into level-by-level work, with one focused worktree, branch, and pull request per task, implemented by subagents using the implement-plan skill.
---

# Iterative implementation

Treat the supplied task map as a dependency graph. Deliver it in small iterations rather than as one large change.

1. Identify every task, its dependencies, and the ready-work levels: level 1 has no dependencies; each later level contains only tasks whose dependencies are in earlier completed levels. Flag missing dependencies and cycles before implementation. If a task references a dependency ID that isn't in the supplied task list, do not invent a level for it or assume it's a real, schedulable task — treat it as an unresolved reference, ask the user to clarify what it is and whether it's already done, and keep only the tasks that depend on it out of the level plan until they answer. Present levels for the rest of the graph in the meantime.
2. Present the resulting tree or level list, including which tasks can run in parallel. Recommend completing one level before beginning the next.
3. Follow the user's requested scope. If they authorize consecutive levels, continue automatically as each prerequisite level completes; otherwise implement only the next ready level.
4. Delegate every selected task to a dedicated subagent. Before it begins implementation, have it update the task's associated issue tracker item to In Progress and assign it to the requesting user; if that item has a parent issue, also move the parent to In Progress. Instruct that subagent to invoke the skill named `wt-switch-create` first, giving it the task's branch name and required base branch, so the task gets its own Worktrunk worktree before any other work starts — never implement directly in the current checkout or branch. Once the worktree is ready, instruct the subagent to invoke `/goal` together with the implement-plan skill — i.e. `/goal` wrapping the implement-plan invocation as its goal — so the subagent only stops once that goal is reached rather than pausing partway through. Provide the task scope, dependency context, required branch base, and one-task-one-PR constraint as part of that invocation. Do not implement a task in the current session.
5. Give every task its own focused worktree, branch, and pull request. Start a task with no dependencies from main; a task with exactly one dependency bases its worktree and branch off that dependency's branch instead. Do not start a task with multiple dependencies until all of them are merged into main; tell the user which prerequisite tasks and branches must be merged, then resume from main once they are available. Each task's worktree keeps its implementation on disk fully separate from the current session's checkout and from every other task's worktree, even when tasks are stacked on one another.
6. Keep each task's implementation, validation, commits, and pull request isolated from other tasks. When opening the task's pull request, instruct its subagent to use the open-pr skill. Do not merge unrelated work into the same branch or PR.
7. After each iteration, report completed tasks, their branches and PRs, validation, newly unblocked tasks, and remaining blockers. Recompute the ready levels when the dependency map changes.

Do not collapse the map into a single implementation or PR, even when multiple tasks are small.
