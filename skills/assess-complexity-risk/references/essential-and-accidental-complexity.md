# Essential and Accidental Complexity

Use the distinction developed by Ben Moseley and Peter Marks in *Out of the Tar Pit* as a decision tool, not as a claim that all complexity can be removed.

## Working definitions

- **Essential complexity** follows from the problem the system has agreed to solve: domain rules, externally imposed constraints, and the guarantees stakeholders choose to retain. It cannot be removed without changing the problem, weakening a guarantee, or violating a real constraint.
- **Accidental complexity** comes from the chosen solution: representation, mutable state, explicit ordering, control flow, synchronization, duplicated knowledge, framework ceremony, or machinery introduced to compensate for other machinery. A different design can reduce it without changing required behavior.

The classification is relative to a stated behavior and boundary. Machinery may be essential to an exactly-once guarantee but unnecessary to the broader user outcome. Say “essential to guarantee X,” not “essential” in the abstract.

## Apply the distinction

For each protected risk:

1. State the domain outcome and the guarantee separately. This exposes guarantees that are implementation-strengthened versions of the actual need.
2. Identify the minimum information the system must retain and the unavoidable decisions it must make to provide that guarantee. Treat this as the essential core until repository evidence disproves it.
3. Trace the state and control machinery around that core. Look especially for mutable state whose history must be understood, ordering protocols, recovery branches, synchronization, and duplicated representations. Classify these as accidental when a simpler representation or declarative rule can preserve the guarantee.
4. Test at least one simpler design that retains the guarantee before proposing to weaken it. A deletion is stronger when it removes accidental complexity without buying risk.
5. If the remaining complexity is inherent to the guarantee, compare that guarantee's user value with its risk-reduction value. Dropping it changes the accepted problem; describe this as a deliberate product or operational tradeoff, not as removal of accidental complexity.

## Decision rule

Prefer outcomes in this order:

1. Preserve the guarantee and remove accidental complexity.
2. Preserve both the guarantee and its essential complexity when the prevented failure is consequential.
3. Accept a narrow, visible, recoverable risk when preventing it requires disproportionate accidental complexity.
4. Reconsider a guarantee itself only when its essential complexity is disproportionate to the value of the guarantee and the resulting risk is explicitly accepted.

Raw LOC is supporting evidence, not the definition of complexity. A short implementation can hide substantial state and control complexity; a longer declarative implementation can be easier to reason about. Count a simplification only when the resulting system has fewer states, transitions, temporal dependencies, representations, or independent rules that must be understood together.

## Source

Ben Moseley and Peter Marks, [*Out of the Tar Pit*](https://curtclifton.net/papers/MoseleyMarks06a.pdf), 2006. The paper identifies complexity—particularly complexity arising from state and control—as the central difficulty in large-scale software and distinguishes complexity inherent in the problem from complexity introduced by the solution.
