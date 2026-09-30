---
name: branch-review-scope
description: Classify code review findings against the current branch's purpose. Use whenever branch-review or branch-review-loop classifies findings, or add-pr-comments needs to classify or interpret review findings.
---

# Classify branch review findings

## Establish the branch purpose

Determine intended scope from the user's task, acceptance criteria or issue, PR title and description, and the reviewed changes. Use those sources as context for the finding. A file being changed by the branch is not, by itself, evidence that every issue in it belongs to the branch.

Classify findings by the change needed to address them, not only by where they appear. A finding can be in scope when the branch introduces or materially affects the behavior, or when a documented requirement calls for the fix. A pre-existing issue in a nearby area remains separate unless the branch makes it relevant to its stated purpose.

## Classifications

- **In-scope**: The fix addresses the branch's purpose or a demonstrated requirement, and can be made without expanding that purpose. It improves correctness, clarity, maintainability, or a requirement established by the task.
- **Follow-up**: The suggestion may be useful, but its benefit is not demonstrated by the branch's requirements, production evidence, profiling, or a reproducible issue. This includes premature performance or concurrency optimization, defensive code for speculative or rare scenarios, and complexity without demonstrated value. Preserve it for later consideration and state what evidence would justify revisiting it.
- **Out-of-scope**: Addressing the finding requires work outside the branch's purpose, such as fixing an unrelated pre-existing issue, doing a broader refactor, or adding a separate feature.

## Explicitly acknowledged exclusions

When the PR description explicitly identifies the same behavior or gap as out of scope or deferred for this PR, classify it as **out-of-scope (acknowledged)**, even if it appears while reviewing changed code. A general mention of a related area is not enough; the description must clearly cover the same issue. This is not a new finding to raise in PR comments. If the implementation conflicts with an explicit requirement, or the review uncovers a concrete impact beyond what the description acknowledges, report that new conflict or impact separately.

Scope is about disposition, not whether a finding is real: retain actionable follow-ups and out-of-scope findings with their classification and reason, except for issues explicitly acknowledged in the PR description. If available context cannot resolve the scope, preserve the finding as an unresolved scope decision; do not treat it as in-scope automatically, and state what decision or evidence is needed.
