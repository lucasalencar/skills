---
name: open-pr
description: Create a new pull request based on the changes made in the current branch.
---

## Steps

1. Resolve the pull request base branch. Use a base supplied by the invoking workflow; otherwise use `main`. For an existing PR, preserve its current base unless the caller explicitly requests a retarget.
2. Check the difference between the current branch and the resolved base branch.
3. Recover any pull request templates if available (`.github` folder).
4. Push local changes in case it wasn't done yet — follow the [commit](../commit/SKILL.md) skill for commit and push instructions.
5. Create the pull request with the resolved base branch using `gh pr create --base <base-branch>`. Always create it as a **draft** (`--draft`) unless the user explicitly asks for a ready-for-review PR.

## Output instructions

- Provide a title and description for the Pull Request.
- State the pull request's base branch when returning the result.
- Text must be in English, unless requested to use another language.
- When branch is referencing some Jira ticket, include the ticket ID in
    the PR title like `[Ticket ID]`.
- Description must follow pull request template available in the repository.
- When returning the Pull Request link, return it as a clickable link in the chat.

## Description style

- Keep the description tight. A reviewer should be able to read it in under a minute and know what to look for in the diff.
- Do **not** enumerate the files changed, list commits, or describe what each commit/file does — that information is in the diff and commit log. Only mention a specific file/symbol when it carries information the diff doesn't make obvious (e.g. a non-obvious cross-module contract).
- Focus each template section on intent, not inventory:
  - **Problem**: the symptom and the root cause, in a few sentences.
  - **Solution**: the shape of the change, not a file-by-file walkthrough.
  - **Rationale**: trade-offs and decisions a reviewer would otherwise ask about (flag gating, scope choices, why X over Y).
- Skip filler that adds no signal (e.g. "lint clean", "tests green", "no public API changes"). Only call these out when they're surprising.
- Prefer linking to tickets/threads for deep context instead of restating it inline.
