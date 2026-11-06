# Skills Repository Instructions

## Workflow

This is a personal repository. It's OK to commit and push directly to `main` — this is the standard workflow for this repo. No need to create feature branches or ask for confirmation before pushing.

## Language

Write all skills and their metadata in English.

## Client-agnostic instructions

Skills must not assume or name a specific client (e.g. "Claude Code", "Codex") in instructions meant to apply universally — write generic terms like "skill" or "subagent" instead of "Claude Code skill". Only mention a specific client when the instruction is genuinely conditional on it (e.g. a step that only exists on one client and must be skipped elsewhere), and even then, scope the client name to that specific branch of logic rather than letting it leak into surrounding wording.

## Skill independence

Keep skills as self-contained and agnostic as possible. Do not reference other skills by name unless it is genuinely necessary (e.g. an intentional workflow handoff where the user expects chaining). When the referenced behavior is short, inline it instead of linking. This keeps each skill isolated and robust against renames.
