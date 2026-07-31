# Test quality

- Assertions that only exercise mock behavior (e.g. verifying that a mock was called, or asserting on values the test itself injected) — these give false confidence because they test the test setup, not the code under test.
- Missing coverage for important scenarios: check whether the tests cover only the happy path, or also exercise meaningful edge cases (empty inputs, boundary values, error conditions). Flag gaps that are likely to hide real bugs, but avoid demanding exhaustive coverage of unlikely or trivial variations.
