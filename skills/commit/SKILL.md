---
name: commit
description: Commit (if necessary) changes on the current branch
---

## Steps

1. Check if current branch is main or master and ask if the user wants to create
   a branch before commiting. Suggest a branch name.
2. Check for changes in the current branch and commit them
3. Ask the user whether they want to push these changes to origin now.
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

- Avoid commiting every unstaged file. Use the chat context to decide
    which changes the user wants to commit.
- Prefer small, focused commits over large ones. When the working tree contains
    multiple distinct changes, split them into separate commits — one per logical
    unit of work — instead of bundling everything into a single big commit.
- Each commit must be atomic and self-contained: it should represent one coherent
    change, leave the project in a working state (not broken mid-refactor), and
    have a message that clearly explains what that specific change does and why.
- The commit history should read as a sensible progression of atomic steps. If
    you find yourself writing a commit message with "and" joining unrelated
    changes, that's a signal to split it into multiple commits.
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
