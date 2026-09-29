# GitHub CLI pitfalls

Use this reference with the shared process in the parent `SKILL.md`. Discover normal command syntax from the `gh` CLI and its `--help` output; avoid treating this file as a command manual.

Keep these GitHub CLI and API pitfalls in mind:

- **Preserve real line breaks in comment bodies.** Include a blank line before the AI-disclosure signature, and send actual newline characters rather than the literal text `\n`. In a shell format string, `printf '%s\n\n%s' "$comment" "$ai_signature"` inserts those newlines.
- **Escape backticks in double-quoted shell variables.** Write them as `\`` so the shell does not interpret them as command substitution; for example, `comment="The \`formatDate\` function"`.
- **Use file line numbers for inline comments.** The GitHub API's `position` field is deprecated and requires counting diff lines. Use `line` and, for a block, `start_line`. Comments on added lines use the new-file side: `side=RIGHT`, and `start_side=RIGHT` for block ranges.
- **Keep block-comment ranges within one diff hunk.** `start_line` must be less than `line`, and both must be in the same hunk. A cross-hunk range can return HTTP 422; use a single-line comment on the last relevant line instead.
- **Match `gh api` field types.** Use `-F` for numeric fields such as `line` and `start_line`, and `-f` for string fields such as `body`, `path`, and `side`.
