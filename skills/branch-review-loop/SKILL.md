---
name: branch-review-loop
description: Iteratively reviews and improves branch changes by running branch-review, applying in-scope fixes, and re-running until no actionable findings remain within the branch scope.
---

## Objective

Run `branch-review` repeatedly, applying in-scope fixes after each iteration, until the review returns no findings that can be addressed within the current branch.

## Steps

1. Run the `branch-review` skill.
2. Classify each finding as **in-scope** or **out-of-scope**:
   - **In-scope**: can be fixed within the current branch without expanding its purpose (bugs, readability issues, test gaps, duplications introduced by this branch).
   - **Out-of-scope**: requires work outside this branch — pre-existing issues, refactors that go beyond the branch's intent, or new features.
3. If there are in-scope findings:
   - Apply all in-scope fixes directly to the code.
   - Commit the changes with a message describing what was fixed.
   - Go back to step 1.
4. If there are no in-scope findings (either no findings at all, or all findings are out-of-scope):
   - Stop the loop.

## Safeguard

Stop after 5 iterations regardless of findings to avoid infinite loops. Report any remaining in-scope findings as unresolved.

## Output

After the loop ends, present:
- A summary of all fixes applied, grouped by iteration.
- Any out-of-scope findings identified but not addressed, with a brief explanation of why they fall outside the branch scope.
