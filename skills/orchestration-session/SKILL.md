---
name: orchestration-session
description: Start an orchestration-only session for a request. Use when the user invokes `/orchestration-session` and wants all task execution and exploration delegated to subagents, keeping the current session focused on orchestration and a high-level view of progress.
---

# Orchestration session

Keep this session exclusively for coordination and a high-level view of the work. Do not research, inspect files, edit code, or use task-execution tools here. Delegate all implementation, investigation, and exploration to subagents.

1. Delegate each request to one or more subagents with clear context, scope, and expected outcome. Use parallel agents when the work has independent parts.
2. Classify each delegated task before dispatch: use a mid-tier model if the task follows a fixed, well-defined procedure (e.g. invoking `ask-pr-review`, `resolve-pr-comments`), or if it has a closed spec (target file/function identified, expected behavior unambiguous, follows an existing pattern) AND is isolated (no reasoning about effects across unrelated files/systems). Otherwise use the client's top-tier model.
3. Tell the user the initial delegation plan, then monitor agents and report meaningful progress, decisions, and blockers without bringing unrelated task details into this session.
4. If the user asks for status, consult the agents and provide a concise high-level update, using the dependency tree below whenever there are more than a couple of tasks or any dependencies between them.
5. When work is complete, consolidate the agents' reports: completed work, conclusions, changed artifacts, validation, and open items.

## Presenting the dependency tree

When status involves more than one or two tasks, or tasks depend on each other, render the plan as a tree using box-drawing characters (`├──`, `└──`, `│`) instead of prose so the user can scan it at a glance. Each node shows the task name and a status tag; children are nested under the task they depend on. When a task has a known Jira card or PR, append its ID/link right after the task name so the user can jump straight to it.

Use these status emojis consistently:
- ⚪ not started — not yet dispatched
- 📝 draft — dispatched but scoped/being defined, not yet doing the core work
- 🔵 in progress — actively being worked on
- 🟡 in review — implementation done, awaiting review/verification
- ✅ done — complete

Example:

```
├── 🔵 Auth migration (PROJ-123)
│   ├── ✅ Design new token schema (PROJ-124)
│   ├── 🔵 Implement token service (PROJ-125, PR #482)
│   │   └── ⚪ Write migration script (PROJ-126)
│   └── 🟡 Update client SDK (PROJ-127, PR #484)
└── ⚪ Docs update (PROJ-128, depends on Auth migration)
```

Keep the tree current as agents change state — regenerate it rather than describing deltas in prose when reporting status. Pull Jira/PR IDs from the agent's own report; do not guess or fabricate an ID if the agent didn't provide one.

## Jira synchronization

When a card has an associated PR, the card's Jira status must track that PR's real state, not just the state you last reported. Each time you gather a status update (per the tree above), transition the Jira card to match:
- PR opened / work started → move the card out of its initial state into in progress (if not already).
- PR opened for review → move the card to in review.
- PR merged and deployed → move the card to done.

Only transition a card when you have direct evidence of the underlying PR state from an agent's report (or your own check) — never advance a card speculatively. If a card's current Jira status already matches, skip the transition. Treat this sync as part of every status update, not a separate step the user has to request.

## Stall management

Periodically check any agent running unusually long. Identify what it's waiting on and confirm the wait is legitimate — i.e. backed by another agent actually producing that output — rather than a dependency that stalled, was never dispatched, or will never resolve. If the wait isn't justified, cancel the stalled agent instead of letting the session idle indefinitely.

Do not replace delegated work with your own execution. If a task cannot be delegated, state that limitation.
