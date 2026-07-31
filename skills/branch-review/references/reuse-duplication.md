# Reuse and duplication

- Code that could be extracted, renamed, or restructured for clarity. Search the codebase for existing patterns, utilities, or abstractions that the new code could reuse instead of reimplementing.
- Repeated boolean or eligibility rules that express the same domain invariant across call sites. Suggest a semantically named pure predicate at the natural domain seam only when verified duplication or meaningful semantic leverage justifies it; do not propose shallow helpers for one-off local conditions. Distinguish the shared invariant from stage-specific checks that should remain near their use. Cite the relevant call sites and suggest the predicate's semantic name and owner.
- Literal values (strings, numbers, identifiers) that duplicate an existing named constant — these create silent drift risk if the canonical definition changes.
- Logic, structure, or patterns introduced or modified in the diff that already exist (or nearly exist) elsewhere in the project.
