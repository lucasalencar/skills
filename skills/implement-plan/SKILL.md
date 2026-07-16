---
name: implement-plan
description: Implement a requested change using test-driven development, commit focused changes, then iteratively review and improve the branch before handing it off. Use only when the user explicitly invokes `$implement-plan`; never load or invoke it automatically.
---

# Implement Plan

## Workflow

1. Invoke the `tdd` skill and use it throughout the implementation.
2. During the implementation, invoke the `commit` skill to commit each complete, focused change. Do not push as part of this workflow.
3. Once the implementation is complete, invoke the `branch-review-loop` skill before presenting the final result.
