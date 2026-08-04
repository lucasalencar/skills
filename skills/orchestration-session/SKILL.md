---
name: orchestration-session
description: Start an orchestration-only session for a request. Use when the user invokes `/orchestration-session` and wants all task execution and exploration delegated to subagents, keeping the current session focused on orchestration and a high-level view of progress.
---

# Orchestration session

Keep this session exclusively for coordination and a high-level view of the work. Do not research, inspect files, edit code, or use task-execution tools here. Delegate all implementation, investigation, and exploration to subagents.

1. Delegate each request to one or more subagents with clear context, scope, and expected outcome. Use parallel agents when the work has independent parts. On Claude Code only: when a request involves multiple stages of the same process (e.g. fan-out then merge, or review → verify → synthesize), use the Workflow tool instead of plain ad hoc subagent calls — the user invoking `/orchestration-session` is itself the explicit opt-in for multi-agent orchestration that tool requires, so proceed without asking again. Workflow gives that multi-stage work deterministic control flow, named phases, and progress grouped under `/workflows`, which plain subagent calls don't provide. This does not apply on other clients, where the Workflow tool does not exist — use plain subagents there as described above.
2. Classify each delegated task before dispatch: use a mid-tier model if the task follows a fixed, well-defined procedure (e.g. invoking `ask-pr-review`, `resolve-pr-comments`), or if it has a closed spec (target file/function identified, expected behavior unambiguous, follows an existing pattern) AND is isolated (no reasoning about effects across unrelated files/systems). Otherwise use the client's top-tier model.
3. Tell the user the initial delegation plan, then monitor agents and report meaningful progress, decisions, and blockers without bringing unrelated task details into this session.
4. If the user asks for status, consult the agents and provide a concise high-level update. If there are more than a couple of tasks or any dependencies between them, load the `iterative-implementation` skill's dependency tree presentation and render status that way.
5. When work is complete, consolidate the agents' reports: completed work, conclusions, changed artifacts, validation, and open items.

## Stall management

Periodically check any agent running unusually long. Identify what it's waiting on and confirm the wait is legitimate — i.e. backed by another agent actually producing that output — rather than a dependency that stalled, was never dispatched, or will never resolve. If the wait isn't justified, cancel the stalled agent instead of letting the session idle indefinitely.

Do not replace delegated work with your own execution. If a task cannot be delegated, state that limitation.
