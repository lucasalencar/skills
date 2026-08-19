---
name: assess-complexity-risk
description: Analyze whether rare failure protections and strong guarantees justify their implementation complexity. Use when evaluating code that handles edge windows, retries, ordering, deduplication, rollover, recovery, or exactly-once-like behavior; when asking what risks could be accepted to simplify a design; or when estimating how much production and test code a proposed simplification would remove.
---

# Assess Complexity Risk

Turn expensive guarantees into explicit tradeoffs. Ground the analysis in the actual code and tests, then recommend the smallest set of accepted risks that deletes meaningful machinery.

Read [`references/essential-and-accidental-complexity.md`](references/essential-and-accidental-complexity.md) before beginning the analysis. Use its essential-versus-accidental distinction throughout the evidence map, candidate comparison, and recommendation.

## Build the evidence map

1. Inspect the implementation, tests, change history, and relevant design documentation. Prefer repository evidence over architectural inference.
2. Trace the normal path and each protected failure window from trigger to outcome.
3. Name every guarantee in user-visible terms, such as “a command arriving while the previous run closes is preserved.”
4. Identify the machinery bought by each guarantee: state, queues, branches, retries, activities, persistence, rollover protocols, and tests. Classify each source of complexity as essential, accidental, or uncertain, and justify the classification relative to the guarantee and domain constraints.
5. Record available frequency and impact evidence. When telemetry is absent, describe the window and exposure qualitatively; do not invent probabilities.

Complete this stage only when every candidate guarantee maps to concrete implementation and test locations.

## Form candidate risks

For each guarantee, state the alternative as a risk the system could deliberately accept:

- Exact failure condition and timing window.
- Observable user or operational impact.
- Recovery path: automatic retry, producer redelivery, user repetition, reconciliation, or no recovery.
- Scope and reversibility of the failure.
- Evidence about frequency, clearly separating measurements from assumptions.

Keep independent risks separate. Split a broad proposal when its parts have different impacts or remove different machinery.

Before weakening a guarantee, look for a design that preserves it while removing accidental complexity. Treat accepting risk as justified by the accidental complexity that remains after plausible simpler designs are considered, not by raw LOC or by complexity essential to the chosen guarantee.

## Measure actual simplification

Trace what becomes unreachable or unnecessary if each risk is accepted. Measure against the current working tree or current `HEAD`, never against a historical commit alone. Commit history may reveal why machinery exists, but later edits can repurpose its code and tests.

Before quoting a LOC estimate, construct the smallest representative patch when safe, or enumerate the exact current symbols and tests that change. Inspect each current test body instead of inferring ownership from its name or originating commit. If neither is possible, label the number as an unvalidated upper bound rather than a reduction estimate.

Report the arithmetic separately:
- Production lines deleted and replacement production lines added.
- Tests deleted and tests required for the new residual behavior added.
- Net production reduction and net total reduction.

Use `git diff --numstat` or an equivalent current-state diff for a prototype. Reconcile the measured result with the estimate before recommending the tradeoff; revise the recommendation when structural simplification produces little or no net deletion.

Count only net deletion after the simpler replacement is included. Include adjacent fixtures, types, configuration, and documentation only when they genuinely disappear. Exclude formatting churn and code merely moved elsewhere.

Classify each proposal:

- **Structural deletion**: removes a state, protocol, queue, persistence boundary, retry loop, or execution path.
- **Local deletion**: removes branches or validation but leaves the surrounding machinery.
- **Semantic weakening**: relaxes a guarantee while retaining nearly all machinery.

Prioritize structural deletion. A weaker guarantee that saves almost no code is not a simplification win.

For every proposal, report how much removed complexity is:

- **Accidental**: caused by representation, coordination, mutable state, control flow, duplicated knowledge, or an implementation choice rather than the problem itself.
- **Essential to the retained behavior**: still required by the domain and remaining guarantees, and therefore preserved or replaced rather than counted as a simplification benefit.
- **Essential only to the dropped guarantee**: unavoidable if that guarantee remains, but removable if product and operations deliberately accept the corresponding risk.

Do not count moving complexity behind an abstraction or into another component as eliminating it. Prefer designs that reduce state and control complexity, not merely line count.

## Account for coupling

Build a dependency map before combining estimates. Mark:

- Shared code and tests removed by multiple candidates.
- Risks that become irrelevant after another cut.
- Replacement logic introduced only by a combination.
- Preconditions that prevent risks from being adopted independently.

Never sum standalone ranges when they overlap. Recalculate each meaningful combination from the resulting design and label uncertainty sources.

## Recommend a proportional cut

Compare candidates across:

| Candidate risk | Failure impact and recovery | Evidence of rarity | Complexity removed | Essential complexity retained | Production deleted/added | Tests deleted/added | Net total | Simplification class | Coupling |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | --- | --- |

Recommend a coherent cut, not automatically the largest deletion. Prefer risks whose failures are narrow, visible, recoverable, and cheap relative to the accidental complexity needed to prevent them. Preserve guarantees whose failures are silent, irreversible, security-sensitive, financially material, or difficult to reconstruct. Preserve essential complexity for retained guarantees; do not present its continued existence as a design failure.

Separate the recommendation into:

1. Risks to accept now.
2. Guarantees to retain.
3. Risks needing telemetry or product agreement.

Explain the resulting simpler state model or flow. State the residual failure behavior plainly enough for product and operations to accept or reject it.

## Add lightweight observability

For accepted risks, propose the cheapest signal that tests the rarity assumption: a counter at the vulnerable transition, a structured log, an alert threshold, or a reconciliation query. Avoid rebuilding the removed reliability mechanism as observability.

Define what evidence would trigger revisiting the decision. Present telemetry as a way to replace uncertainty with data, not as proof that an unmeasured event is rare.

## Deliver the analysis

Lead with the recommended cut and estimated net reduction. Then provide the candidate table, overlap-adjusted combinations, evidence gaps, residual risks, and observability plan. Cite concrete files or symbols for estimates whenever a repository is available.
