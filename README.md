# Skills

This repository brings together all the skills I use across the various AI Agents in my daily workflow.

Skills are instructions and prompts that extend the capabilities of AI agents, enabling them to perform specific tasks more efficiently.

## About the skills

The skills here are personal — developed and refined through my own experience with AI Agents. Some of them are inspirations or adaptations of interesting skills shared by the community online. Where applicable, the original source is credited within the skill itself.

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
| [improve-codebase-architecture](skills/improve-codebase-architecture/SKILL.md) | Find deepening opportunities in a codebase. Surfaces architectural friction and proposes refactors that turn shallow modules into deep, testable, AI-navigable ones. |
| [open-pr](skills/open-pr/SKILL.md) | Create a new pull request based on the changes in the current branch, following repository PR templates and conventions. |
| [pr-review](skills/pr-review/SKILL.md) | Perform a Pull Request review, checking for bugs, typos, security flaws, performance issues, and simplification opportunities. |
| [resolve-pr-comments](skills/resolve-pr-comments/SKILL.md) | Fetch Pull Request comments and resolve them by applying suggested changes or replying with reasoning when a suggestion conflicts with prior decisions. |

## Contributing

This is a personal repository, but feel free to draw inspiration from the skills shared here.