---
name: commit
description: Use this skill whenever you are about to commit changes for the user — ALWAYS load it before running `git commit`, whether the user explicitly asked for a commit or it's a step within a larger task. Covers branch checks, splitting into atomic commits, and push confirmation.
---

## Steps

1. Check the repository workflow and current branch before committing. Follow
   repository-local instructions for branch and push policy.
2. Build a **commit inventory** before staging anything:
   - Inspect `git status`, the complete diff, and the staged diff.
   - Account for every intended changed hunk in a short list of independently
     reviewable changes. Give each change a one-sentence intent that includes
     its outcome and reason.
   - Treat changes as independent when either can be reviewed, reverted, or
     cherry-picked without the other. Put them in separate commits, even when
     they touch the same file.
   - Group changes only when they form one inseparable behavior: one would leave
     the project broken, misleading, or incomplete without the other. Include
     directly supporting tests, documentation, and configuration in that same
     commit.
3. Commit the inventory one change at a time. For each change:
   - Stage only its files or hunks, using `git add -p` whenever a file contains
     more than one inventory item.
   - Inspect `git diff --cached` and verify that it contains exactly that
     change's intent and no unrelated hunks.
   - Run the relevant validation when it is available and proportionate.
   - Commit it with a message that explains the specific outcome and why it is
     needed, then continue with the next inventory item.
   - Re-check the remaining unstaged diff before starting the next commit; a
     new distinct intent creates a new inventory item and commit.
4. Finish only when `git diff --cached` is empty and every intended hunk is
   either committed in its own appropriate unit or intentionally left unstaged
   with a stated reason.
5. Ask the user whether they want to push these changes to origin now.
   - If auto-push mode is already active for this session (see below), skip
     this question and push automatically instead.
   - If they say yes, push, then enable auto-push mode: from this point on,
     keep pushing automatically after every commit made in this session
     (whether via this skill or otherwise) without asking again, until the
     user explicitly says to stop.
   - If they say no, do not push, and do not enable auto-push mode.
   - Default is not to push: if the user invokes the skill without specifying
     a push preference and doesn't give a clear answer to this question, do
     not push and do not enable auto-push mode.

## Guidelines

- Do not stage the whole working tree by default. The commit inventory, rather
  than file boundaries or convenience, defines each commit boundary.
- Atomicity is required, not a preference: each commit contains one intent and
  all of its direct support. A reviewer must be able to describe its purpose in
  one sentence without using unrelated clauses.
- Write messages around intent. The subject states the outcome; add a concise
  body whenever the subject does not also make the reason clear. The body should
  capture motivation, behavioral impact, or a material decision—not an
  implementation transcript.
- The history should be a sensible progression of independently useful steps.
  Before committing, test the proposed boundary with this question: “Could this
  change be reverted or reviewed separately without changing the meaning of the
  other changes?” If yes, split it.
- **A single file may contain multiple unrelated changes.** Do not assume "one
  file = one commit". Inspect each modified file's diff (e.g. `git diff <file>`)
  and look for distinct logical units — unrelated edits in different regions of
  the same file must be split into separate commits, one per logical change.
  Use `git add -p` (patch mode) to stage hunks individually when you need to
  separate changes inside the same file. If two edits in the same file belong
  to different iterations or different intents, they belong in different commits.

## Output instructions

- Check previous commits to decide which language to use on commit
    messages and branch names. Default is English.
