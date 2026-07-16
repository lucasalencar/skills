# Skills

This repository brings together all the skills I use across the various AI Agents in my daily workflow.

Skills are instructions and prompts that extend the capabilities of AI agents, enabling them to perform specific tasks more efficiently.

## Installation

Install the skills for a specific tool with:

```bash
./scripts/install <agent>
```

For Codex, this creates symbolic links by default in `$CODEX_HOME/skills` (or
`~/.codex/skills` when `CODEX_HOME` is unset):

```bash
./scripts/install codex
```

Use `./scripts/install` to auto-detect installed tools, or
`./scripts/install all` to install for every supported tool. The installer uses
symbolic links (`--method=ln`) by default, so edits in this repository are
available immediately. Use `--method=cp` to make independent copies; rerun the
installer after any skill changes in that case.

## About the skills

The skills here are personal — developed and refined through my own experience with AI Agents. Some of them are inspirations or adaptations of interesting skills shared by the community online. Where applicable, the original source is credited within the skill itself.

Some skills are synced from external sources:
- [Matt Pocock's skills repository](https://github.com/mattpocock/skills) — a great open collection of AI agent skills
- [Hunk's skills repository](https://github.com/modem-dev/hunk) — specialized skills for code review and development workflows

## Structure

```
skills/
  ├── <skill-name>/
  │     └── README.md   # skill description and instructions
  └── ...
```

## Skills

| Skill | Description |
|-------|-------------|
| [ask-pr-review](skills/ask-pr-review/SKILL.md) | Request a Pull Request review. Runs a fixed baseline (improve description, mark ready) then executes team-specific custom steps. Learns each team's workflow on first use. |
| [assess-change-impact](skills/assess-change-impact/SKILL.md) | Analyze a code change for non-obvious ripple effects across the system. Use before merge to surface semantic shifts, symmetric code paths, and latent bugs hidden behind a seemingly local change. |
| [commit-push](skills/commit-push/SKILL.md) | Commit (if necessary) and push changes to the origin branch, with guidance on branch naming and commit splitting. |
| [grill-me](skills/grill-me/SKILL.md) | Interview you relentlessly about a plan or design, resolving each branch of the decision tree until reaching shared understanding. |
| [hunk-review](skills/hunk-review/SKILL.md) | Interact with live Hunk diff review sessions via CLI. Inspects review focus, navigates files and hunks, and adds inline review comments for interactive diff review. |
| [improve-codebase-architecture](skills/improve-codebase-architecture/SKILL.md) | Find deepening opportunities in a codebase. Surfaces architectural friction and proposes refactors that turn shallow modules into deep, testable, AI-navigable ones. |
| [implement-plan](skills/implement-plan/SKILL.md) | Explicitly invoked implementation workflow: use test-driven development, then review and improve the branch until no in-scope findings remain. |
| [open-pr](skills/open-pr/SKILL.md) | Create a new pull request based on the changes in the current branch, following repository PR templates and conventions. |
| [pr-review](skills/pr-review/SKILL.md) | Perform a Pull Request review, checking for bugs, typos, security flaws, performance issues, and simplification opportunities. |
| [resolve-hunk-comments](skills/resolve-hunk-comments/SKILL.md) | Fetch the review comments the user left in a live Hunk session and address them in the current code. |
| [resolve-pr-comments](skills/resolve-pr-comments/SKILL.md) | Fetch Pull Request comments and resolve them by applying suggested changes or replying with reasoning when a suggestion conflicts with prior decisions. |

## Syncing from external sources

Skills are synced from external repositories using dedicated scripts. Each script clones the source repo into `.sources/` (gitignored) on first run, then pulls updates on subsequent runs, and copies the selected skills into `skills/`.

### Matt Pocock's skills

```bash
./scripts/sync-mattpocock-skills
```

To change which skills are synced, edit the `SKILLS_TO_SYNC` array in `scripts/sync-mattpocock-skills`.

### Hunk's skills

```bash
./scripts/sync-hunk-skills
```

To change which skills are synced, edit the `SKILLS_TO_SYNC` array in `scripts/sync-hunk-skills`.

## Contributing

This is a personal repository, but feel free to draw inspiration from the skills shared here.
