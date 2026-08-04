---
name: orchestration-session
description: Coordinate a request exclusively through delegated subagents while keeping the current session focused on planning, routing, progress, and synthesis. Use only when the user explicitly invokes `/orchestration-session` or `$orchestration-session` and wants all investigation and execution delegated.
---

# Orchestration session

Act only as the coordinator. Delegate investigation, implementation, artifact inspection, validation, and other task execution. In this session, use only orchestration capabilities and information returned by subagents; do not inspect or modify task artifacts or independently reproduce their work.

## Workflow

1. Divide the request only as much as needed for effective delegation. Give each subagent clear context, scope, constraints, and an expected outcome.
2. Tell the user the initial delegation plan. Keep it brief and revise it when agents uncover material changes.
3. When the client supports model selection, choose based on reasoning complexity, ambiguity, and risk rather than task size alone. Use faster or lower-cost models for bounded procedural work with clear acceptance criteria; use more capable models for ambiguous, cross-cutting, high-risk, or synthesis-heavy work.
4. Delegate independent parts in parallel when capacity permits. Sequence parts only when one genuinely depends on another, and route required results between agents.
5. Avoid assigning multiple agents to modify the same artifacts concurrently unless their ownership boundaries are explicit and non-conflicting.
6. Monitor the delegated work and report meaningful progress, decisions, blockers, or changes in scope. Answer status requests from agent reports rather than performing the work directly.
7. When useful, delegate independent verification and distinguish its findings from claims reported by the agent that performed the work.
8. At completion, consolidate the agents' reports: completed work, conclusions, changed artifacts, validation, limitations, and open items.

## Stall management

Check agents that run unusually long or stop reporting progress. Ask for status and identify the exact wait condition. Route missing inputs, redirect a stuck approach, or replace the assignment when needed. Stop an agent only when its work is obsolete, duplicated, or cannot make progress.

Do not replace delegated work with your own execution. If required work cannot be delegated with the available capabilities, report the limitation and ask the user how to proceed.
