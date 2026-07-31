# Maintainability

Reason about where this implementation closes off future change versus where it preserves optionality, and whether those choices match what the domain actually warrants.

- **Accidental rigidity**: Places where a specific decision unnecessarily seals an extension point — a hardcoded value where it may vary, a concrete dependency where an interface would have preserved flexibility, a data shape that conflates two concerns that are likely to diverge.
- **Unnecessary abstraction**: The inverse — indirections that add complexity but protect flexibility that is unlikely to be needed. If the code is generic where it could simply be specific, flag it: premature flexibility is a maintainability cost just like premature rigidity.
- **Silent assumptions and hidden coupling**: Two places that share an implicit contract (an ordering, a naming convention, an enumeration's completeness, a format) without enforcing it. When the contract changes, the second site breaks without warning.
- **Irreversible commitments presented as local decisions**: Schema migrations, persistent formats, public API shapes, or naming decisions that downstream systems will depend on. When a decision will be expensive to reverse, the code should make that cost visible rather than hide it behind what looks like an implementation detail.
