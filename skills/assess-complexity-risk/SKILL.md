---
name: assess-complexity-risk
description: Analyze whether a change's complexity and scope are proportionate to its core user outcome. Use whenever the user wants to evaluate complexity vs. risk or identify scope that can be cut — triggers include "avaliar complexidade", "vale a pena essa complexidade", "simplificar design", "analyze complexity risk", "retries/ordering/deduplication really needed", "what risks could we accept", "is this beyond the core feature", or wants to estimate code removed by simplification.
---

# Assess Complexity Risk

Turn expensive guarantees into explicit tradeoffs. Ground the analysis in the actual code and tests, then recommend the smallest set of accepted risks that deletes meaningful machinery.

Read [`references/essential-and-accidental-complexity.md`](references/essential-and-accidental-complexity.md) before beginning the analysis. Use its essential-versus-accidental distinction throughout the evidence map, candidate comparison, and recommendation.

## Establish the core outcome and scope

Before tracing failure protections, establish what user outcome the change is meant to deliver and which capabilities it adds:

1. Read the PR description, linked issue or design, and relevant product or repository documentation. Treat stated intent as evidence, not proof; use the implementation and tests to establish what the change actually delivers.
2. State the core user outcome in one sentence, independently of the chosen implementation. Identify the smallest coherent capability that would deliver meaningful value to the intended user.
3. Inventory the distinct capabilities added by the change. Classify each as **core**, **required support** for the core outcome, **scope expansion** that adds value beyond the core, or **uncertain**. Explain each classification with evidence. A capability is required support if removing it would break the core flow, contract, or usable delivery; do not call it optional just because it can be described separately.
4. Trace dependencies between capabilities. Note when an apparent extra is coupled to core behavior, provides a necessary contract or safety property, or would require replacement work if cut.
5. For each plausible scope cut, describe the smallest coherent version that retains the core outcome, which capabilities and machinery disappear, what user value is deferred, and what new limitations or follow-up work result. Treat a cut as a product tradeoff, not automatically as a defect in the PR.

Use scope analysis alongside failure-risk analysis throughout the review. Do not focus only on rare failures or local edge cases: for a broad change, assess whether the additional capabilities justify their implementation, interaction, and maintenance costs relative to the core outcome. Do not assume that a capability is a nice-to-have merely because a smaller feature can ship without it; validate that judgment against the stated user need and available evidence.

## Build the evidence map

1. Inspect the implementation, tests, change history, and relevant design documentation for every major capability and its dependencies. Prefer repository evidence over architectural inference.
2. Trace each core and expanded user path from entry point to observable outcome, then trace the normal path and each protected failure window from trigger to outcome.
3. Name every guarantee in user-visible terms, such as “a command arriving while the previous run closes is preserved.”
4. Identify the machinery bought by each capability and guarantee: state, queues, branches, retries, activities, persistence, rollover protocols, UI and API surface, and tests. Classify each source of complexity as essential, accidental, or uncertain, and justify the classification relative to the user outcome, guarantee, and domain constraints.
5. Record available frequency and impact evidence. When telemetry is absent, describe the window and exposure qualitatively; do not invent probabilities.

Complete this stage only when the core outcome and every material scope candidate and guarantee map to concrete implementation and test locations, with dependencies and evidence gaps recorded.

## Form candidate risks

For each guarantee, state the alternative as a risk the system could deliberately accept:

- Exact failure condition and timing window.
- Observable user or operational impact.
- Recovery path: automatic retry, producer redelivery, user repetition, reconciliation, or no recovery.
- Scope and reversibility of the failure.
- Evidence about frequency, clearly separating measurements from assumptions.

Keep independent risks separate. Split a broad proposal when its parts have different impacts or remove different machinery.

Before weakening a guarantee, look for a design that preserves it while removing accidental complexity. Treat accepting risk as justified by the accidental complexity that remains after plausible simpler designs are considered, not by raw LOC or by complexity essential to the chosen guarantee.

For scope cuts, first verify that the core outcome remains coherent and usable after the cut. Prefer deferring an independently valuable capability when it can be removed cleanly and the retained core still solves the intended user problem. Do not recommend a cut whose replacement work, lost contract, or weakened safety behavior erases the apparent simplification or undermines the core outcome.

## Measure actual simplification

Trace what becomes unreachable or unnecessary for each proposed risk or scope cut. For a scope cut, show how the retained feature still delivers the core outcome. Measure against the current working tree or current `HEAD`, never against a historical commit alone. Commit history may reveal why machinery exists, but later edits can repurpose its code and tests.

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

For every proposal, including scope cuts, report how much removed complexity is:

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

| Candidate cut or risk | Type | Core outcome retained | User value or guarantee deferred | Impact and recovery / supporting evidence | Complexity removed | Essential complexity retained | Production deleted/added | Tests deleted/added | Net total | Simplification class | Coupling |
| --- | --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | --- | --- |

Recommend a coherent cut, not automatically the largest deletion. For reliability risks, prefer risks whose failures are narrow, visible, recoverable, and cheap relative to the accidental complexity needed to prevent them. Preserve guarantees whose failures are silent, irreversible, security-sensitive, financially material, or difficult to reconstruct. For scope, prefer cuts that defer additional capabilities while preserving the core outcome and a complete usable path. Preserve essential complexity for retained guarantees and required support; do not present its continued existence as a design failure.

Separate the recommendation into:

1. Scope to retain as the core outcome and required support.
2. Scope expansion to cut or defer, with the value and limitations that change.
3. Risks to accept now.
4. Guarantees to retain.
5. Risks or scope decisions needing telemetry, product evidence, or owner agreement.

Explain the resulting smaller feature boundary and, where applicable, simpler state model or flow. State the user-facing behavior that remains, what is deferred, and any residual failure behavior plainly enough for product and operations to accept or reject it.

## Add lightweight observability

For accepted risks, propose the cheapest signal that tests the rarity assumption: a counter at the vulnerable transition, a structured log, an alert threshold, or a reconciliation query. Avoid rebuilding the removed reliability mechanism as observability.

Define what evidence would trigger revisiting the decision. Present telemetry as a way to replace uncertainty with data, not as proof that an unmeasured event is rare.

## Deliver the analysis

Lead with the core outcome, recommended scope boundary, and estimated net reduction. Then provide the candidate table, overlap-adjusted combinations, evidence gaps, residual risks, and observability plan. Distinguish scope-cut candidates from accepted reliability risks in the table and recommendation. Cite concrete files or symbols for estimates whenever a repository is available.
