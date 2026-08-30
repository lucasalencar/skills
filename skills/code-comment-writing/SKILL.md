---
name: code-comment-writing
description: Write, revise, or remove source-code comments and test descriptions to capture context the code cannot express. Use whenever the user wants to add or clean up comments — triggers include "adicionar comentário no código", "melhorar comentários", "code comments", "docstring", "documentar função", "limpar comentários", or wants to review excessive/redundant commentary.
---

# Code comment writing

Treat code as the primary documentation. Add a comment only to preserve context that a careful reader cannot recover from the code itself.

## Apply the context test

For each candidate comment, identify the fact it would add. Keep it only when that fact is not apparent from names, types, structure, control flow, tests, or the surrounding code. Prefer making the code clearer when that resolves the ambiguity.

Write the smallest complete statement of the missing context. Remove comments that merely restate the code or its obvious intent.

## Choose the right comment

### Inline comments

Use an inline comment to explain a non-obvious reason for an operation or choice: a constraint, compatibility behavior, safety property, trade-off, or rejected alternative. Place it immediately beside the decision it explains.

State the reason, not a line-by-line account of the operation.

```python
# Keep the original order: callers use the first matching rule as precedence.
for rule in rules:
    if rule.matches(request):
        return rule
```

### Function documentation

Document a function only when a brief statement clarifies its non-obvious purpose or contract. Before adding a usage example, determine whether an executable test should demonstrate that usage instead. Prefer a test when it can document the contract while protecting it from regressions. Leave implementation narration, historical origin, and routine behavior to the code and its call sites.

### Test-case descriptions

Let the test name, fixture setup, assertions, and exercised code express the behavior under test. Add a brief test description or comment only when it preserves context that the test cannot make clear on its own: why the scenario matters, the regression it prevents, or a non-obvious boundary being protected.

Describe that context concisely. Do not restate business rules or narrate the assertions when the test already makes them clear.

### Module documentation

Use a concise module docstring when it helps establish the module's purpose or boundary. Summarize why the module exists and the context in which it belongs. Do not duplicate business rules that are expressed by the implementation.

## Review comments before keeping them

- Does the comment give the reader information unavailable in the code?
- Does it explain why rather than repeat what happens?
- For a function usage example, would an executable test document the contract more usefully?
- For a test, does it add the scenario's importance or the regression being prevented beyond what the test name and assertions show?
- Is it short enough to be read as part of the code?
- Would clearer code eliminate its need? If so, improve the code when that is within scope; otherwise, keep only the essential explanation.
- Is its location adjacent to the decision or interface it clarifies?
