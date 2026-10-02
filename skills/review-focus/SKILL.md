---
name: review-focus
description: Prepare a visual, human-led review guide for a PR, branch, or change set. Use when the user wants change context, an ordered file-reading path, or help deciding which business and architectural questions need human judgment; use branch-review for an automated findings-focused code review.
---

# Review focus

Create a **review briefing** that brings the reviewer up to speed before directing their judgment. Deliver it as a self-contained HTML file and open it when complete. The briefing is an orientation and decision aid, not a verdict, an endorsement of the implementation, or an exhaustive file-by-file diff summary.

## Establish the change and its intent

Resolve the review range before interpreting the diff:

1. Honor a range, PR, branch, or fixed point supplied by the user.
2. Otherwise, use the open PR's base branch when one exists.
3. Otherwise, compare the current branch with its actual base branch. If that cannot be established safely, ask the user for the intended range.

Read the PR title and description when available, along with relevant issue, design, or repository documentation. Treat these as claims about intent, not proof that the implementation is correct. Read the diff broadly, then trace the code, configuration, tests, and callers needed to explain every consequential decision selected for review.

## Build one coherent story

Work backward from the decisions the reviewer should make. Select the small set of changes where human contextual judgment is most valuable, then gather enough context for the reviewer to reason about each one without first reconstructing the implementation.

The briefing has three primary sections, in this order:

1. **Context** teaches the system concepts, before/after behavior, flows, boundaries, and implementation details needed by the next section.
2. **Review map** gives the reviewer an ordered path through the small set of files that best explain the change.
3. **Review focus** presents only the prioritized decisions and questions that deserve the reviewer's attention.

Connect the sections explicitly. The map should build on the context and prepare the reader for the review questions. Every review point must link back to the relevant context block, and every substantial context block must prepare the reader for at least one review point. Arrange the context, map, and review points in a shared narrative where practical. The reader should never jump from a superficial overview into an unexplained implementation detail.

Remain independent from the implemented solution. Describe what the code does and why it appears to do it, distinguishing repository evidence from PR-stated intent and from inference. Give the reviewer enough understanding to challenge the chosen design; do not lead them toward approving it.

## Section 1: Context

Prefer visual explanation over prose. Choose the smallest set of visuals that makes the consequential behavior clear; do not add decorative diagrams. Useful forms include:

- a before/after flow for changed behavior or ownership;
- a sequence diagram for interactions, retries, events, or lifecycle;
- a state diagram or decision table for rules and transitions;
- a dependency or boundary map for architectural changes;
- a compact data-shape comparison for contracts and schemas.

Use Mermaid when it communicates the relationship well and the source could be reused in documentation. Prefer a clearer HTML/CSS table, timeline, annotated code path, or inline SVG when that better serves understanding. Mermaid reuse is secondary to review clarity.

Keep prose compact and favor bullets. Begin with a short orientation that states the goal and boundary of the change without evaluating it. Then explain the relevant flow at the depth required by the review points. Label important implementation choices, unchanged behavior, assumptions, and uncertainty. Link visual nodes, captions, and supporting bullets to the narrowest relevant changed locations when useful.

Do not expose a question in Review focus whose underlying actors, terms, path, or behavior have not been introduced in Context. A mechanically simple change may need only one compact visual or structured summary.

## Section 2: Review map

Give a practical, ordered reading path through the change's principal files. This is a comprehension order: it tells the reviewer where to start and how to follow the story across the codebase. It is distinct from the consequence-based priority order in Review focus. Include only files that materially explain changed behavior or establish a contract; do not reproduce the changed-file list.

Choose this path from the actual flow and evidence in the diff, not alphabetical order or directory layout. For each step:

- link directly to the changed file in the PR when available, using the changed-location link rules below; otherwise use the closest reliable repository link and never invent a URL;
- name the region or behavior to read, and say whether the reviewer should read the whole file or a focused range;
- explain what the step establishes and how it leads to the next step.

Order files to make the behavior easiest to understand. For example, start with tests when their scenarios clearly establish the expected behavior, then follow the entry point through core logic and downstream effects. Use another order when the implementation, contract, or data flow provides a clearer story. For a cohesive core file, direct the reviewer to read it from beginning to end when that gives better understanding than hopping between isolated hunks. Keep the path short and omit incidental files.

If the change has no meaningful multi-file story, keep the map proportionate: give a single step for its principal file or a brief note that the change can be read directly in one location. Do not invent a sequence to fill space.

## Section 3: Review focus

Produce one strict priority order: item 1 is the best next use of the reviewer's attention and every later item is lower priority. Rank by consequence and uncertainty, not file size, discovery order, or diff order. Prefer three to seven items; use fewer when the change is simple and more only for independently consequential decisions.

Investigate only dimensions the diff actually raises, such as:

- business rules, permissions, state transitions, defaults, and exception paths;
- API, event, schema, persistence, migration, integration, flag, configuration, and rollout contracts;
- ownership, coupling, dependency direction, abstraction, consistency, and future evolution;
- behavior-preserving claims, deletions, refactors, and the invariants they must retain;
- predicates, ordering, fallbacks, error policy, authorization, and lifecycle;
- product intent, operational policy, acceptable trade-offs, and ownership that the repository cannot settle.

For each item include:

- the decision or tension, phrased neutrally rather than as a suspected defect;
- why it deserves human judgment and why it has this priority;
- one or more concrete questions the reviewer can answer from product, domain, architecture, or operational context;
- links to the relevant context block and narrow changed locations;
- a terse evidence note separating fact, stated intent, and inference when ambiguity exists.

Use tests as evidence of intended behavior. Mention them only when their cases expose a decision, leave a meaningful path unproven, or encode an assumption the reviewer should validate.

Present questions after their supporting rationale, not as detached prompts. Do not include low-value changed files, generic praise, implementation summaries that belong in Context, automated findings, or speculative defects merely to fill the list.

## Links to changed locations

When reviewing an open PR, link every selected location, including Review map files, to that PR's **Files changed** view. Do not substitute a branch or head-commit link while a PR URL is available. For a whole-file reading step, use the file's diff anchor without a line anchor; use a line anchor for a focused range when its line is known.

For GitHub, construct the location link from the PR URL: `PR_URL/files#diff-<SHA-256 of the PR-relative path>R<new-line>`. Use `L<old-line>` for a removed line. For a file without an anchorable line, retain the `#diff-...` file anchor without `R` or `L`. Hash the path shown by the PR diff: post-change for additions or modifications and pre-change for deletions.

For another provider, use its closest reliable PR file-diff link. If no file anchor can be established, link to Files changed and show `path:line` beside it. Never invent a URL or line anchor.

## HTML artifact

Write one responsive, self-contained `.html` file. Default to a clearly named file in the operating system's temporary directory so the reviewed repository remains clean; honor a user-specified destination. The page must remain understandable if scripts or network resources fail.

Design for focused reading:

- a compact header identifies the change, review range, and generation time;
- a sticky or compact navigation links to all three primary sections and numbered review points;
- restrained color, typography, spacing, and visual hierarchy make the story easy to scan;
- cards and callouts encode meaning consistently, with labels for fact, intent, inference, and uncertainty;
- code and paths wrap or scroll without breaking the layout;
- print styles produce a usable document;
- accessibility includes semantic headings, sufficient contrast, text equivalents, and reduced-motion behavior.

Embed CSS and any hand-authored SVG. If Mermaid is useful, include its diagram source in the HTML and render it when a Mermaid runtime is available; retain a readable source or textual fallback. Avoid dependencies whose absence makes the briefing unusable.

Open the completed file with the platform's normal browser-opening mechanism. If the environment requires authorization for opening a local file, request it at that point. In chat, return only a concise completion note with the file link and any essential limitation; the briefing itself belongs in the HTML.

## Completion criteria

Before opening the file, verify that:

- every review point is evidence-backed, strictly prioritized, and prepared by linked context;
- the review map follows a clear comprehension order, names whole-file or focused reading, and links to the relevant changed files;
- the context covers no substantial material that is irrelevant to the review points;
- the reviewer can distinguish observed behavior, stated intent, and inference;
- the visuals explain the consequential flows and remain comprehensible with Mermaid or JavaScript unavailable;
- every external and changed-location link is valid to the extent the provider permits;
- the HTML opens locally, is readable at narrow and wide widths, and contains the three promised primary sections.
