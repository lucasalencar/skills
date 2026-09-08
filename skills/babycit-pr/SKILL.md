---
name: babycit-pr
description: Continuously monitor a Pull Request's CI, review activity, and divergence from its base branch; fix actionable failures and feedback, and safely rebase a clean branch. Use when the user wants a PR babysat or continuously polled, including "babysit PR", "babysit do PR", "BabyCit PR", "watch the PR", "monitor PR", "monitorar PR", or wants CI, comments, and branch freshness watched together.
---

## Objective

Run a persistent PR watch for the requested duration (12 hours by default;
allow up to 24 hours when requested). Keep the PR head branch healthy:
required CI must pass on its current head SHA, all actionable discussion and
review activity must be handled, and the branch must be brought current with
`main` whenever that can be rebased cleanly. A push, re-run, or
successful rebase starts a new evaluation of the resulting head SHA.

Use `scripts/poll_pr.py` for low-overhead remote polling. It emits JSON Lines
only for the initial snapshot and material state changes; leave it running in
a persistent terminal session and react when it prints an event. It requires
the authenticated GitHub CLI (`gh`) and is intentionally read-only.

## Progress reporting

The user is waiting on this watch — never act silently. Narrate the loop:
- **What happened**: every state transition (check flipped, new comment
  arrived, new sha pushed) gets a short update as soon as it is detected.
  Silence is only acceptable when a poll shows literally nothing new.
- **What changed and why it matters**: quote the failing step / error lines
  for red checks; quote or paraphrase each new comment with author and
  location. Do not just say "CI failed" or "new comment" — say what failed
  and what was asked.
- **What you will do next**: announce the planned action and its reason
  *before* acting ("re-running job X because it looks like a runner
  timeout", "applying Y's suggestion on file Z because ...", "pausing for
  your decision on ... because it expands scope").
- **What the action produced**: report the outcome right after (re-run
  queued/passed, commit sha pushed, reply posted, loop resuming on new sha).
- Keep each update to a few lines: event, meaning, next action. Full detail
  goes only in the final summary (see Output).

## Steps

1. **Resolve the target PR.**
   - Use a PR number/URL supplied by the invoking workflow; otherwise use the
     PR associated with the current branch.
   - If there is no open PR for the branch and the user expected one, stop
     and say so instead of guessing.
   - Record the PR head branch and sha being watched; if the sha changes
     mid-watch (new push), restart evaluation against the new sha.
   - Verify that the PR targets `main`. If it targets another branch, report
     that fact and ask whether that branch should replace `main` as the
     update source; do not silently rebase onto a different target.

2. **Establish the baseline and start the watcher.**
   - Detect which CI system the PR uses (e.g. `gh pr checks`, `gh run list`,
     or the forge's check API for the PR head sha). Do not assume a specific
     provider — use whatever CLI/API the repository already uses.
   - List all required checks and their current state
     (pending / passing / failing). Report the baseline briefly before
     entering the loop.
   - Snapshot every existing issue comment, review submission, and inline
     review comment. Treat unaddressed actionable feedback already on the PR
     as work, then mark handled item IDs so unchanged items are not revisited.
   - Start `python3 scripts/poll_pr.py <PR> --duration 12h --interval 120` in a
     persistent terminal session. Use a shorter interval only when it is
     useful, and pass a user-requested duration up to 24 hours. The script is
     an event source, not a replacement for diagnosis: inspect changed data
     with `gh` when it emits an event.

3. **Enter the watch loop.**
   - React to each watcher event by polling the authoritative forge data.
     If the helper is unavailable, poll at a sensible interval (a few minutes
     for remote CI; shorter only for fast local-equivalent suites).
     Per Progress reporting above: stay quiet only when nothing changed;
     every transition or new comment gets an immediate update.
   - On each poll with news, report: which checks flipped state since the
     last poll, the current tally (e.g. "3 passing, 1 pending, 1 failing"),
     and any new comments since the last poll (author + what was asked).
   - Keep watching for the whole requested duration, even when CI is green
     and no feedback is currently open. Move to step 4 as soon as a required
     check fails, step 5 as soon as actionable feedback appears, and step 6
     when the PR falls behind its base branch. Handle one event at a time,
     then re-poll before acting on the next — a fresh push may resolve several
     events.

4. **Diagnose each failure.**
   - Fetch the failure logs for the failed check/run only (full log for
     small suites; failing step/tail for large ones). Prefer the
     provider's CLI (e.g. `gh run view --log-failed`) over re-running
     locally first.
   - Classify the failure before acting:
     - **Flake / infra**: timeout, runner lost, network/DNS blip, rate
       limit, out-of-disk, service unavailable, or a test that passes on
       retry without code changes.
     - **Code issue in this PR**: test failure, lint/type error, or build
       break caused by the PR's own changes.
     - **Broken base / external**: failure on files the PR did not touch,
       upstream dependency breakage, or expired secrets/tokens the agent
       cannot rotate.
     - **Needs human decision**: ambiguous ownership, policy/security
       sign-off, or a fix that would expand the PR's scope.
   - State the classification and the evidence (failing step, error lines)
     before acting, as part of the "what changed / what you will do" update —
     never push or re-run before announcing it.

5. **Address each actionable comment.**
   - For every actionable item found in the baseline or since the last poll,
     run the
     `resolve-pr-comments` triage process (which itself follows
     `resolve-review-comments` and `pr-comment-writing`): read the code at
     the comment's location, classify intent (question / suggestion / mixed),
     and evaluate suggestions technically before acting — never apply on the
     reviewer's word alone.
   - Reply where that process says to reply (answers to questions,
     reasoning when declining), and apply justified code changes directly.
     Announce each comment's verdict (apply / reply / decline + why) before
     acting. Batch all comment-driven fixes from the same poll into a single
     commit and push following the `commit` skill, reporting the sha pushed,
     then return to step 3 against the new sha.
   - Scope-expanding suggestions and ambiguous feedback pause the loop:
     surface what the reviewer asked, why it grows the branch scope or needs
     judgment, and wait for the user's decision instead of pushing a guess.
     Mark already-triaged comment ids as seen so re-polls do not reprocess
     them; treat replies from the PR owner as new events only if they request
     further changes.

6. **Update a stale branch safely.**
   - When the PR is behind `main`, fetch `main` and confirm
     the working tree is clean. Check whether applying the PR commits onto
     that fetched `main` has a conflict before changing history (for example,
     use `git merge-tree --write-tree HEAD <remote>/main` as a preflight).
   - Only when that preflight is clean, announce the exact base SHA, rebase
     onto it, verify the resulting branch, and push with `--force-with-lease`.
     Re-check that the remote head is still the SHA evaluated before rebasing;
     if it changed, abandon the attempt and return to the watch loop.
   - If the preflight reports conflicts, leave the branch untouched, report
     the conflicting paths and that a human rebase is required, then continue
     observing CI and comments. Do not start a rebase that is expected to
     conflict, and never resolve conflicts automatically.
   - A clean rebase creates a new PR SHA: return to step 3 and wait for CI on
     that SHA before considering the branch healthy.

7. **Act on the failure classification.**
   - **Flake / infra**: re-run only the failed jobs/checks (never the full
     matrix unless the provider lacks per-job rerun), then return to step 3.
     Cap blind re-runs at 2 per check — a third identical failure is treated
     as a real failure, not a flake.
   - **Code issue in this PR**: announce the fix plan first, then fix the
     code directly, verify with the narrowest local reproduction available
     (single test, lint on touched files), then commit and push following the
     `commit` skill, reporting what was fixed and the new sha. Return to
     step 3 against the new sha.
   - **Broken base / external** or **needs human decision**: stop the loop
     and report — do not push speculative fixes outside the PR's scope.

8. **Respect loop safeguards.**
   - Stop at the requested time limit (12 hours by default, never more than
     24 hours). There is no fixed cap on genuine fix rounds; instead, stop
     and ask for direction when repeated attempts cannot produce new evidence
     or a fix would require a human decision.
   - Never push when the working tree has unrelated uncommitted changes —
     ask the user how to proceed instead.
   - Never retarget, merge, or close the PR. Rebase only when the invoking
     request authorizes the clean-rebase workflow described in step 6.

## Output

- At the time limit: confirm the final PR SHA and base SHA, per-check status,
  whether the branch is current, comments addressed (applied / replied /
  declined with reasoning), and every fix, re-run, or rebase pushed. Link the
  PR and state whether it is currently merge-ready.
- When blocked: report per-check status, the failing step and
  key log lines for each red check, unaddressed comments and what they need,
  what was already tried (re-runs, fixes pushed), and the specific decision
  or action needed from the user.
