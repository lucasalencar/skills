# Performance

- Algorithmic complexity blowups introduced by the diff (e.g. accidental O(n²) over a collection that can grow large).
- N+1 query patterns, redundant recomputation, missing batching/pagination.
- Blocking/synchronous calls introduced on hot or latency-sensitive paths.
- Unbounded memory growth (unbounded caches, accumulating buffers, loading full datasets where streaming would do).
