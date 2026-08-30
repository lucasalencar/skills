---
name: branch-review-loop
description: Iteratively review and auto-fix branch changes by running branch-review in a loop. Use only when the user explicitly invokes this skill (e.g. "/branch-review-loop", "$branch-review-loop", "roda o branch-review-loop"); never load automatically on generic review requests. Use branch-review for normal reviews.
---

## Objective

Run `branch-review` repeatedly, applying only justified in-scope fixes after each iteration, until the review returns no findings that should be addressed within the current branch. Keep the resulting PR focused and reviewable; do not add defensive complexity for speculative or rare scenarios.

## Steps

1. Run the `branch-review` skill in full — every iteration of this loop, including the second, third, and beyond, must invoke all of the subagent skills that `branch-review` specifies. Do not shortcut later iterations to a single subagent or a subset; each pass through step 1 is a brand-new, complete `branch-review` run.
2. Classify each finding as **in-scope**, **follow-up**, or **out-of-scope**:
   - **In-scope**: can be fixed within the current branch without expanding its purpose and improves correctness, clarity, maintainability, or a demonstrated requirement.
   - **Follow-up**: proposes premature performance or concurrency optimization, extra defensive code for speculative or rare scenarios, or complexity whose benefit is not demonstrated by the branch's requirements, production evidence, profiling, or a reproducible issue. Do not implement it in this loop; record it for later consideration.
   - **Out-of-scope**: requires work outside this branch — pre-existing issues, refactors that go beyond the branch's intent, or new features.
3. If there are in-scope findings:
   - Apply all justified in-scope fixes directly to the code.
   - Commit the changes with a message describing what was fixed.
   - Go back to step 1.
4. If there are no in-scope findings (either no findings at all, or all findings are follow-ups or out-of-scope):
   - Stop the loop.

## Safeguard

Stop after 7 iterations regardless of findings to avoid infinite loops. Report any remaining in-scope findings as unresolved.

## Output

After the loop ends, present:
- A summary of all fixes applied, grouped by iteration.
- Follow-ups not implemented, especially premature performance or concurrency optimizations, with the triggering comment and the evidence needed before reconsidering them.
- Any out-of-scope findings identified but not addressed, with a brief explanation of why they fall outside the branch scope.
- A short list of pending decisions that require the user's attention — trade-offs, ambiguous scope calls, or findings that could go either way.
