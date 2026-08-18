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

To remove stale installed symlinks and install the current skills in one step,
run:

```bash
./scripts/sync-skills <agent>
```

Omit `<agent>` to auto-detect installed tools. Any install options, such as
`--method=cp`, are passed through to `scripts/install`.

## About the skills

The skills here are personal — developed and refined through my own experience with AI Agents. Some of them are inspirations or adaptations of interesting skills shared by the community online. Where applicable, the original source is credited within the skill itself.

Some workflows depend on skills installed through the `mattpocock-skills` plugin. See [Matt Pocock's skills repository](https://github.com/mattpocock/skills) for the source and installation options.

Some skills are synced from [Hunk's skills repository](https://github.com/modem-dev/hunk).

## Structure

```
skills/
  ├── <skill-name>/
  │     └── SKILL.md   # skill description and instructions
  └── ...
```

## Skills

| Skill | Description |
|-------|-------------|
| [add-pr-comments](skills/add-pr-comments/SKILL.md) | Add line-specific review comments to a GitHub Pull Request. |
| [ask-pr-review](skills/ask-pr-review/SKILL.md) | Request a Pull Request review. Runs a fixed baseline (improve description, mark ready) then executes team-specific custom steps. Learns each team's workflow on first use. |
| [assess-change-impact](skills/assess-change-impact/SKILL.md) | Analyze a code change for non-obvious ripple effects across the system. Use before merge to surface semantic shifts, symmetric code paths, and latent bugs hidden behind a seemingly local change. |
| [branch-review](skills/branch-review/SKILL.md) | Review branch changes across multiple dimensions and analyze their impact. |
| [branch-review-loop](skills/branch-review-loop/SKILL.md) | Iteratively review and improve branch changes until no actionable findings remain. |
| [commit](skills/commit/SKILL.md) | Check, split, commit, and optionally push focused changes safely. |
| [debug-local-servers](skills/debug-local-servers/SKILL.md) | Investigate local development servers through their tmux pane logs. |
| [hunk-review](skills/hunk-review/SKILL.md) | Interact with live Hunk diff review sessions via CLI. Inspects review focus, navigates files and hunks, and adds inline review comments for interactive diff review. |
| [implement-task](skills/implement-task/SKILL.md) | Explicitly invoked implementation workflow: use test-driven development, then review and improve the branch until no in-scope findings remain. |
| [iterative-implementation](skills/iterative-implementation/SKILL.md) | Coordinate dependency-ordered Jira tasks through isolated subagents, worktrees, branches, and Pull Requests. |
| [open-pr](skills/open-pr/SKILL.md) | Create a new pull request based on the changes in the current branch, following repository PR templates and conventions. |
| [orchestration-session](skills/orchestration-session/SKILL.md) | Coordinate a request exclusively through delegated subagents. |
| [pr-comment-writing](skills/pr-comment-writing/SKILL.md) | Define how to write concise Pull Request comments and replies. |
| [resolve-hunk-comments](skills/resolve-hunk-comments/SKILL.md) | Fetch the review comments the user left in a live Hunk session and address them in the current code. |
| [resolve-pr-comments](skills/resolve-pr-comments/SKILL.md) | Fetch Pull Request comments and resolve them by applying suggested changes or replying with reasoning when a suggestion conflicts with prior decisions. |
| [resolve-review-comments](skills/resolve-review-comments/SKILL.md) | Apply a shared triage process to code review comments. |
| [spin-off-branch](skills/spin-off-branch/SKILL.md) | Extract independent work into a new branch based on main. |
| [work-checkout-message](skills/work-checkout-message/SKILL.md) | Generate a prioritized, Slack-ready summary of open Pull Requests. |

## Syncing from external sources

Skills are synced from external repositories using dedicated scripts. Each script clones the source repo into `.sources/` (gitignored) on first run, then pulls updates on subsequent runs, and copies the selected skills into `skills/`.

### Hunk's skills

```bash
./scripts/sync-hunk-skills
```

To change which skills are synced, edit the `SKILLS_TO_SYNC` array in `scripts/sync-hunk-skills`.

## Contributing

This is a personal repository, but feel free to draw inspiration from the skills shared here.
