---
name: pr-review
description: Perform a Pull Request review, analyzing changes from the current branch compared to its base branch.
---

## Execution

Before doing anything else, check whether the current conversation has any prior messages (i.e., messages exchanged before this skill was invoked). If there are no prior messages, run the analysis directly in this context — no subagent is needed. If there are prior messages, delegate the entire review to a subagent (via the Agent tool) without passing any current conversation context, to ensure the analysis is unbiased and not influenced by prior conversation history.

When delegating to a subagent, copy the full text of every section of this skill verbatim into the subagent prompt — do not summarize, paraphrase, or omit any section. The subagent must receive identical instructions to what is written here.

Once the subagent finishes, relay its complete output to the user exactly as returned — do not summarize, compress, or rewrite it. The subagent's response is the final output of this skill.

## Steps

1. Determine the base branch: run `gh pr view --json baseRefName -q .baseRefName`. If that fails, fall back to `main`.
2. Fetch the PR diff, description, and comments.
3. Review the diff against each dimension below and list all findings.

## Review dimensions

**Correctness**
- Bugs, typos, security flaws, and performance issues.
- For error handling and retry paths, verify that each attempt has a real chance of succeeding differently — check that any state mutations or side effects from the failed attempt are undone before retrying, and that error messages accurately reflect whether recovery actually occurred.

**Readability**
- Premature optimizations that trade readability for performance.
- Code that is hard to read at a glance — long functions, deeply nested conditionals, or names that describe implementation rather than intent. Suggest extractions or renames that would let a reader understand what the code does without having to trace through how it does it.

**Maintainability**

Reason about where this implementation closes off future change versus where it preserves optionality, and whether those choices match what the domain actually warrants.

- **Accidental rigidity**: Places where a specific decision unnecessarily seals an extension point — a hardcoded value where it may vary, a concrete dependency where an interface would have preserved flexibility, a data shape that conflates two concerns that are likely to diverge.
- **Unnecessary abstraction**: The inverse — indirections that add complexity but protect flexibility that is unlikely to be needed. If the code is generic where it could simply be specific, flag it: premature flexibility is a maintainability cost just like premature rigidity.
- **Silent assumptions and hidden coupling**: Two places that share an implicit contract (an ordering, a naming convention, an enumeration's completeness, a format) without enforcing it. When the contract changes, the second site breaks without warning.
- **Irreversible commitments presented as local decisions**: Schema migrations, persistent formats, public API shapes, or naming decisions that downstream systems will depend on. When a decision will be expensive to reverse, the code should make that cost visible rather than hide it behind what looks like an implementation detail.

**Reuse and duplication**
- Code that could be extracted, renamed, or restructured for clarity. Search the codebase for existing patterns, utilities, or abstractions that the new code could reuse instead of reimplementing.
- Literal values (strings, numbers, identifiers) that duplicate an existing named constant — these create silent drift risk if the canonical definition changes.
- Logic, structure, or patterns introduced or modified in the diff that already exist (or nearly exist) elsewhere in the project.

**Test quality**
- Assertions that only exercise mock behavior (e.g. verifying that a mock was called, or asserting on values the test itself injected) — these give false confidence because they test the test setup, not the code under test.
- Missing coverage for important scenarios: check whether the tests cover only the happy path, or also exercise meaningful edge cases (empty inputs, boundary values, error conditions). Flag gaps that are likely to hide real bugs, but avoid demanding exhaustive coverage of unlikely or trivial variations.

## Output instructions

- List identified issues clearly without modifying the code.
- For refactoring and duplication findings, reference the specific file and line number of the existing code in the project that is relevant.
- Use the same language as the conversation.
