---
name: review-focus
description: Prepare a human-led review guide for a PR, branch, or change set. Use when the user wants help deciding what to inspect most carefully, the important changes in a large diff, or the business and architectural decisions that need human judgment; use branch-review for an automated findings-focused code review.
---

# Review focus

Create a **review map**: a compact, evidence-backed guide that helps a human spend attention on the consequential parts of a change. The goal is orientation and judgment, not an automated verdict or a file-by-file diff summary.

## Establish the change and its intent

Resolve the review range before interpreting the diff:

1. Honor a range, PR, branch, or fixed point supplied by the user.
2. Otherwise, use the open PR's base branch when one exists.
3. Otherwise, compare the current branch with its actual base branch. If that cannot be established safely, ask the user for the intended range.

Read the PR title and description when available, along with relevant issue, design, or repository documentation. Treat these as context for the review, not as proof that the implementation is correct. Read the diff broadly first, then trace only the code, configuration, tests, and callers needed to understand its meaningful changes.

## Build the review map

Select the small set of changes where a human's contextual judgment is most valuable. Produce one strict priority order: item 1 is the first thing the reviewer should inspect and every later item is lower priority. Rank by consequence and uncertainty, not by file size, discovery order, or diff order. A small edit can be the top priority when it changes a boundary, default, policy, or interpretation.

Investigate the dimensions the diff actually raises. Useful signals include:

- a business rule, eligibility condition, pricing or permission decision, state transition, default, or exception path whose intended behavior must be affirmed;
- a contract or boundary change: API, event, schema, persistence, migration, integration, feature flag, configuration, or rollout behavior;
- an architectural decision affecting ownership, coupling, dependency direction, abstraction, consistency with neighboring paths, or the ability to evolve the system;
- a behavior-preserving claim, refactor, deletion, or test change where the preserved invariant deserves explicit confirmation;
- a small but semantically dense change, especially one that alters a predicate, ordering, fallback, error policy, authorization, or lifecycle;
- an ambiguity the repository cannot resolve: product intent, acceptable trade-off, operational policy, or ownership.

For each selected item, verify the claim from the change and surrounding code. Explain why it matters in the language of the system, link to the relevant changed location, and pose a concrete review question. Surface uncertainty honestly: a question is valuable when it directs the reviewer to a decision only they can make.

When reviewing an open PR, include a clickable link for every selected location. Prefer the code-hosting provider's PR diff URL anchored to the changed line or range. If that anchor cannot be established reliably, link to the file at the PR head commit and include the line number in the link. If neither URL is available, retain the `path:line` reference; never invent a URL or line anchor. Link the narrowest changed location that provides enough context for the reviewer to understand the decision.

Use tests as evidence of the behavior the author intended to preserve or introduce. Call out a test only when its cases reveal a business decision, leave a meaningful path unproven, or encode an assumption the reviewer should validate.

## Output

Start with a one-paragraph change narrative: what the change appears to accomplish and its main boundary of effect. Then present a numbered review map in strict priority order. The reviewer must be able to read from top to bottom knowing each item is the next best use of their attention. Prefer three to seven items; exceed that only when the change genuinely contains more independently consequential decisions.

For every item include:

```markdown
### 1. Highest priority — concise decision or change

**Inspect:** [`path/to/file:line`](https://host.example/pull/123/files#changed-line) and the relevant symbol or flow.

**Why this deserves attention:** The concrete behavior, invariant, or trade-off at stake.

**Priority rationale:** Why this comes before the remaining items.

**Review question:** A question the reviewer can answer from product, domain, architecture, or operational context.

**Evidence:** The specific diff or surrounding-code fact that led to this focus.
```

End with a short **Suggested reading path** that follows the same priority order and groups the most important files or flows in a useful sequence. Use the same links there when they make the path easier to follow. It should help the reviewer avoid mechanically traversing every changed file. Also name material changes that were examined but do not need special human attention, when that helps establish scope.

Keep the report concise and actionable. Do not manufacture concerns to fill categories, duplicate an automated code-review report, or present speculative defects as findings. When the change is mechanically simple, say so and identify the single decision, if any, worth validating.
