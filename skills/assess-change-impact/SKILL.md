---
name: assess-change-impact
description: Analyze a code change for non-obvious ripple effects across the rest of the system. Use after AI-generated edits, before merge, to surface semantic shifts, symmetric code paths, test fixture antipatterns, and latent bugs hidden behind a change that looks local. Language- and project-agnostic. Trigger when the user asks for "impact analysis", "what else could break", "did this change anything else", "review the blast radius of these changes", or wants a pre-merge safety check on AI-generated edits.
---

## Execution

Before doing anything else, check whether the current conversation has any prior messages (i.e., messages exchanged before this skill was invoked). If there are no prior messages, run the analysis directly in this context — no subagent is needed. If there are prior messages, delegate the entire impact analysis to a subagent (via the Agent tool) without passing any current conversation context, to ensure the analysis is unbiased and not influenced by prior conversation history.

When delegating to a subagent, copy the full text of every section of this skill verbatim into the subagent prompt — do not summarize, paraphrase, or omit any section. The subagent must receive identical instructions to what is written here.

Once the subagent finishes, relay its complete output to the user exactly as returned — do not summarize, compress, or rewrite it. The subagent's response is the final output of this skill.

## Goal
Given a code change, identify what could break or behave differently in the rest of the system as a consequence — including effects the diff does not make obvious. The intended reader is someone about to merge or deploy: they want a short, specific list of risks they should look at, not a procedural report.

**Use for:** non-trivial changes, especially anything touching shared utilities, parsers/serializers, dispatching logic, wire formats, persisted data, or symbols called from multiple sites.

**Skip for:** typo fixes in dead code, single-line config tweaks with obviously local scope, edits confined to a private function with one caller.

## Method

The agent decides what to investigate based on the actual change and codebase. There is no fixed checklist. The discipline is in **how** the investigation is done, not in covering a predefined list of items:

1. **Read the diff first, then form hypotheses about what could be affected.** Do not start by running a generic checklist — start by understanding what semantically changed and reasoning about who or what depends on that.

2. **Verify, do not speculate.** Every claim about callers, dependencies, or invariants must be backed by a search, a file read, or a tool result. If something cannot be verified, say so explicitly — do not assert.

3. **Prefer specific over comprehensive.** A short list of concrete, verified risks beats a long list of possibilities. If a category turns up empty, say it turned up empty — do not pad.

4. **Think beyond the diff.** The change may have ripple effects in code the diff does not touch (callsites, sibling code paths with the same pattern, fixtures, snapshots, docs, monitoring queries, downstream consumers, persisted state, etc.). It is the agent's job to surface those.

5. **Distinguish blocking from informational.** Some findings should block the merge; others are follow-ups. Label them so the reader knows what to act on now.

## Common dimensions worth considering

Not a checklist — a starting menu. The agent should add, drop, or invent dimensions based on what the change actually touches. If the change involves a category not listed here, investigate it; if a listed category is irrelevant, skip it without comment.

- **Semantic shifts:** what behavior changed, including refactors that claim "no behavior change" (verify the claim)
- **Callers and consumers:** who depends on what changed, and whether their assumptions still hold
- **Dispatching changes:** for any matching/routing/lookup that changed, what newly matches and what stopped matching, and whether real-world inputs land in those sets
- **Symmetric code paths:** input parser vs output builder, reader vs writer, encoder vs decoder — do they still agree?
- **Sibling code:** other handlers/adapters/modules with the same shape as the one changed — do they share the same latent bug, or the same fix opportunity?
- **Tests and fixtures:** are fixtures derived from an authoritative source (upstream schema, captured real sample) or copied from the code under test? The latter can hide bugs on both sides.
- **Production vs test paths:** feature flags, config gates, env-specific branches — does the test setup exercise the same path as production?
- **Preserved invariants:** what should NOT have changed (API signatures, wire formats, error contracts, performance class, concurrency guarantees, resource lifecycle) — verify each.
- **Cross-cutting concerns:** logging volume/level, metrics correctness, DB/migration safety, security (input validation, deserialization, authz), backward compatibility across rolling deploys, persisted data shape.
- **Scope creep / latent bugs:** patterns the change reveals (or fixes) that may exist elsewhere in the codebase as separate, untouched instances.

If the change touches something not in this list (e.g. a build system, a UI framework, an ML pipeline, a query optimizer), invent the relevant dimensions for that domain.

## Output

A short report. Reader should be able to act on each item in under a minute.

- Group findings by severity. Suggested buckets: **blocking** (must address before merge), **medium** (worth a closer look, may become a follow-up), **low / hygiene** (nice to fix, not urgent), **preserved invariants** (explicit confirmation of what still holds). Adapt the buckets to the change.
- For each finding: state the risk, cite specific files/symbols/lines, and propose an action.
- Order by blast radius, not by where in the diff the issue surfaces.
- End with a short list of suggested follow-ups, ranked by ROI, marking which are blocking vs which can become tickets.
- Match the language the user used; default English.

## Anti-patterns to avoid

- Padding the report with generic possibilities ("might affect performance", "could have security implications") that were not actually investigated
- Citing dimensions that do not apply to the change just to show coverage
- Asserting things about the codebase that were not verified by a tool call
- Producing a long, narrative document when a tight list would serve the reader better
