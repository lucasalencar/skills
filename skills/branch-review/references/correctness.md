# Correctness

- Bugs, typos, off-by-one errors, incorrect logic, and unhandled edge cases.
- For error handling and retry paths, verify that each attempt has a real chance of succeeding differently — check that any state mutations or side effects from the failed attempt are undone before retrying, and that error messages accurately reflect whether recovery actually occurred.
