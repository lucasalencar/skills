# Readability

- Premature optimizations that trade readability for performance.
- Long functions that combine multiple conceptual steps or branches. Identify cohesive stages that can become helper functions with intent-revealing names, so the top-level function reads as an outline of the operation. Flag this especially when a reader must keep state from earlier branches in mind to understand later ones; do not suggest mechanical extractions that merely move lines without clarifying responsibility or control flow.
- Deeply nested conditionals or names that describe implementation rather than intent. Suggest extractions, guard clauses, or renames that let a reader understand what the code does without tracing through how it does it.
