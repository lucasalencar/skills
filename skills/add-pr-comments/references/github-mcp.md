# GitHub MCP pitfalls

Use this reference with the shared process in the parent `SKILL.md`. Discover normal operation names and arguments from the GitHub MCP tool descriptions and schemas available in the current environment.

Keep these MCP-specific pitfalls in mind:

- **Tool names, schemas, and capabilities vary.** Inspect the available descriptions and input schemas for each run. Map the needed operation to the exposed fields; do not guess names, arguments, or assume an unsupported operation exists.
- **Inline location fields vary.** A tool may accept file line numbers, diff positions, or a side/range model. Follow its schema, target a line in the PR diff, and verify the returned path and location (fetch the comment if the create response omits them). Keep block ranges within one hunk, with the start before the end. If range comments are unsupported, use one line at the end of the relevant block.
- **Review submission may be a separate step.** Some tools create pending review comments that must be submitted; others publish immediately. When supported, put the out-of-scope summary in the review-level body and submit it with the in-scope comments as one comment-only review. Follow the exposed lifecycle and avoid submitting an empty review, duplicate summary comment, or unrelated review state.
- **General comments and inline review comments are different operations.** For a file outside the PR diff, use a general PR comment and include its path and line in the body; do not force an inline comment onto it.
- **Editing and deletion may be unavailable.** If an existing comment needs an update but the MCP server exposes no edit operation, do not create a duplicate; report that the update could not be made. Likewise, report any unavailable read, create, validation, or delete operation instead of assuming success.
- **Use MCP for the whole GitHub operation in this environment.** Do not switch to `gh` or another GitHub route when an MCP operation is missing; state the specific capability that is unavailable.
