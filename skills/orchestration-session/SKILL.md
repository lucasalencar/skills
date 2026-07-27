---
name: orchestration-session
description: Start an orchestration-only session for a request. Use when the user invokes `/orchestration-session` and wants all task execution and exploration delegated to subagents, keeping the current session focused on orchestration and a high-level view of progress.
---

# Orchestration session

Keep this session exclusively for coordination and a high-level view of the work. Do not research, inspect files, edit code, or use task-execution tools here. Delegate all implementation, investigation, and exploration to subagents.

1. Delegate each request to one or more subagents with clear context, scope, and expected outcome. Use parallel agents when the work has independent parts.
2. Tell the user the initial delegation plan, then monitor agents and report meaningful progress, decisions, and blockers without bringing unrelated task details into this session.
3. If the user asks for status, consult the agents and provide a concise high-level update.
4. When work is complete, consolidate the agents' reports: completed work, conclusions, changed artifacts, validation, and open items.

Do not replace delegated work with your own execution. If a task cannot be delegated, state that limitation.
