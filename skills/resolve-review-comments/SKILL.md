---
name: resolve-review-comments
description: Shared triage process for reviewer comments on a code change — classify intent, evaluate suggestions, decide whether to apply, apply with a note, or ask. Use when another skill needs to process comments left on a code review, regardless of source (GitHub PR, a Hunk session, etc.).
---

# Resolve Review Comments

The shared process for working through reviewer comments on a code change. Source-specific skills (fetching comments, replying, marking resolved, committing) should load this skill and run this process per comment — don't re-derive the triage logic per source.

## Process

For each comment:

1. **Read context.** Look at the code at the comment's location plus surrounding code, and any related history (plan, prior conversation, codebase patterns).

2. **Classify intent:**
   - **Question** — the reviewer is asking something (design, behavior, naming, intent) — not necessarily requesting a change.
   - **Suggestion** — the reviewer is proposing a concrete code change.
   - **Mixed** — both a question and an implicit suggestion.

3. **Handle questions:**
   - Try to answer it from the code and context.
   - If the answer is clear, record/reply with the explanation — no code change unless the answer reveals a real problem.
   - If it can't be answered from available context, bring it to the user before doing anything else. Only proceed with a change after the question is resolved and it's clear one is warranted.

4. **Handle suggestions.** Perform a technical evaluation before acting — never apply on the reviewer's word alone:
   - Read the actual code at the relevant location.
   - Assess whether the suggestion is correct, necessary, and beneficial given the current implementation.
   - If it conflicts with previous decisions (conversation history, plan, codebase patterns), factor that in — explain the reasoning instead of blindly applying.
   - Classify and act:
     - **Apply automatically** — clearly correct and confirmed by the code (obvious bugs, simple improvements, clear style fixes). Apply without asking.
     - **Apply with note** — sound but involves trade-offs worth surfacing. Apply and record the reasoning.
     - **Ask the user** — ambiguous, has significant downsides, or can't be fully evaluated from the code alone. Pause and ask before proceeding.

5. **Mixed comments** — address the question per step 3 and the suggestion per step 4. Answering the question is not a substitute for evaluating the suggestion, and vice versa.

## What this skill does not cover

Fetching comments, navigating to them, replying/threading, marking resolved, committing, and output format are all source-specific — the calling skill owns those. This skill only covers steps 1-5: read, classify, evaluate, act.
