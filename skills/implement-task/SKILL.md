---
name: implement-task
description: Implement a task using test-driven development, focused commits, iterative branch review, and a pull request. Use whenever the user asks to implement a task or ticket, including when another workflow delegates implementation.
---

# Implement Task

## Workflow

1. Invoke the `tdd` skill and use it throughout the implementation.
2. During the implementation, invoke the `commit` skill to commit each complete, focused change.
3. Once the implementation is complete, invoke the `branch-review-loop` skill. Run it on the client's top-tier model — it requires deep understanding of the code and its relationships.
4. After the review loop completes, invoke the `open-pr` skill to open the PR, using the base supplied by the invoking workflow when applicable. Report the PR and validation results.
