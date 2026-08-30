---
name: work-checkout-message
description: Generate a daily/weekly checkout message listing the user's open PRs grouped by priority and dependency order. Use only when the user explicitly invokes this skill (e.g. "/work-checkout-message", "$work-checkout-message", "checkout message", "mensagem de checkout"); never load automatically on generic PR or review requests.
---

# Checkout message

Build a message the user can paste into Slack (or similar) summarizing every open pull request they authored, so teammates know what to review and in what order. This is a personal workflow tool, not scoped to the current repo — the user's open PRs may be spread across several repositories.

## 1. Fetch the user's open PRs across all repos

Use `gh search prs` rather than `gh pr list`, since the latter is scoped to one repo:

```
gh search prs --author=@me --state=open --json repository,number,title,url,body,labels,updatedAt
```

This is the full candidate list. Only include PRs that are open and ready for review: exclude drafts, since a draft isn't ready for someone to look at yet and including it would misrepresent the checkout.

## 2. Pull per-PR detail needed for dependency detection

`gh search prs` doesn't expose base/head branch. For each PR, fetch it individually:

```
gh pr view <number> -R <owner/repo> --json baseRefName,headRefName,body,comments
```

You need this to detect stacking (step 4) and to have the full body/comments text for dependency phrases the search summary might have truncated.

## 3. Classify each PR as high or low priority

Judge priority from what the PR actually does, read from its title/body/diff intent — not from asking the user to manually tag every single one (that gets tedious fast and defeats the point of automating this).

- **High priority**: new functionality, or a fix for a bug that has real user/customer impact.
- **Low priority**: docs changes, minor/cosmetic bug fixes, test-only improvements, refactors. These are worth reviewing but aren't blocking anything the team is tracking.

Labels can help confirm a classification if the repo uses them consistently (e.g. `bug`, `priority`, `tech-debt`), but don't assume every repo has useful labels — the PR title, description, and linked issue are the primary signal.

When a PR is genuinely ambiguous (e.g. a bug fix where impact isn't clear from the description), ask the user briefly rather than guessing — a wrong high/low call undermines the whole point of the message.

Priority is contagious upward through dependencies: once you've built the dependency graph in step 4, any PR that a high-priority PR depends on (directly or transitively) becomes high priority too, even if its own content looks like a refactor or minor fix. A refactor that's just laying groundwork for an important feature is functionally part of that feature's critical path — nobody can review the important PR without it, so it can't sit in the "if you have time" bucket. Do this promotion after building the dependency graph, then run steps 5–6 on the corrected classification.

## 4. Detect dependencies between PRs

A PR depends on another when either is true:

- **Stacked branch**: its `baseRefName` matches the `headRefName` of another PR in the candidate list (i.e., it's built on top of another of the user's unmerged PRs, not on `main`/`master`).
- **Explicit reference**: its title, body, or comments mention another PR or issue in dependency language — "depends on #123", "blocked by #123", "stacked on #123", "on top of #123", etc. Resolve `#123`-style references against the candidate list (same repo) to confirm they point at another PR being included in this message; a reference to something already merged or outside this list isn't a live dependency.

Build a small dependency graph from these edges: PR B depends on PR A means A must be reviewed first.

## 5. Order each priority bucket by dependency

Within the high-priority list and separately within the low-priority list, topologically sort so that every PR appears after everything it depends on. A PR with no dependencies and nothing depending on it keeps its natural order (e.g. most recently updated first, or whatever order `gh search prs` returned). Because priority was already promoted upward through dependencies in step 3, every dependency edge should now stay inside a single bucket — if one still crosses buckets, double check the promotion was applied correctly before treating it as an exception.

If you detect a cycle (shouldn't normally happen, but PR text can be messy), don't silently drop it — tell the user which PRs seem mutually dependent and ask them to clarify the intended order.

## 6. Write the message

Output plain text suitable for pasting directly into Slack — no markdown headers or `#`/`##` syntax, since Slack doesn't render them. Use simple section labels, bullets, and Slack's own emphasis syntax (`*bold*`) if useful. Keep each PR to one line: repo (if the user has PRs across multiple repos), title, link, and — only when it adds signal — a short note like "(stacked on #123)" or "(blocks the migration in #456)".

Write the message in English by default, regardless of the language the request came in — switch only if the user asks for another language.

Start with a short intro line — one sentence naming this as the daily/weekly PR checkout and, loosely, how many PRs are up for review. Sprinkle a couple of emoji through the message (intro line, section labels) to match how the team actually talks in Slack — but keep it light, one or two per section is plenty; a wall of emoji reads as noise, not friendliness.

Example shape:

```
👋 Here's today's PR checkout — 4 PRs up for review.

🔴 *High priority*
• [repo] Add rate limiting to the ingest API — <link>
• [repo] Fix crash on empty payload (stacked on the PR above) — <link>

🟢 *Low priority*
• [repo] Refactor retry logic — <link>
• [repo] Update README for new config flags — <link>
```

Adjust the two section labels if the user prefers different wording (e.g. "Needs review this week" / "If you have time"), and mention in the message header whether it's the daily or weekly checkout if the user specifies which one they're running.

## 7. Confirm before posting anywhere

Show the drafted message in the conversation first — don't post it anywhere automatically. Posting to Slack is visible to the whole team and hard to un-send, so it always needs an explicit go-ahead:

1. Present the full message text and ask if it looks right, or if the user wants any PR moved between sections, reordered, or reworded.
2. Ask whether to post it to Slack at all — the user may just want the text to paste themselves.
3. If they want it posted, ask which channel, unless they already named one in their request. Don't guess or default to a channel silently, since posting to the wrong channel is the kind of mistake that's awkward to walk back.
4. Only after the channel is confirmed, send the message (see the Slack messaging skill for how to post).
