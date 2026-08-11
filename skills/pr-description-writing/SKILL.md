---
name: pr-description-writing
description: Draft or improve a Pull Request description that introduces a code change through its problem, importance, concise solution summary, and decision rationale. Use when writing, revising, or reviewing a PR description for clarity, concision, and context beyond the diff.
---

# Pull Request description writing

Write a compact introduction to the diff. Help reviewers understand why the change exists and why its shape is appropriate; let the diff explain the mechanical implementation.

## Gather the context

Read the issue, incident, request, or conversation that motivated the change. Inspect the diff only enough to identify the solution's meaningful decisions and scope. Ask for missing context only when it prevents explaining the problem or rationale accurately.

## Draft the description

Use this structure when all sections add value:

```markdown
## Problem

<What is wrong, missing, or limited, and why it matters.>

## Solution

<One or two sentences that summarize the approach.>

## Rationale

- <Decision or solution element> because <reason it fits the problem or constraint>.
- <Decision or solution element> because <reason it fits the problem or constraint>.
```

Omit empty or redundant sections. Keep the result short, direct, and objective.

## Content rules

- Make the problem concrete and state its impact or importance. The description must establish why the PR exists, not merely name the symptom.
- Summarize the solution at the level of approach. Preserve implementation details for the diff unless they explain a non-obvious decision.
- Use rationale bullets to connect consequential choices to their motivations: constraints, trade-offs, safety, product intent, or expected behavior.
- Mention scope only when it clarifies the boundary of the change or a deliberate exclusion.
- Mention a file, module, or component only when it is essential context for understanding the change. Treat the diff as the source of truth for ordinary file-level changes.

## Quality check

- Can a reviewer identify the problem and why it matters without reading the diff?
- Does the solution state the approach without retelling visible code changes?
- Does each rationale bullet explain a decision that is not self-evident from the diff?
- Would removing a sentence make the description less useful? Remove it if not.
- Does the description orient the reviewer to the diff rather than attempt to replace it?
