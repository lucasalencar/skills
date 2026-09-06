---
name: babysit-ci
description: Monitor a Pull Request's CI checks and incoming review comments until CI is green and feedback is addressed, investigating failures and fixing or re-running as needed. Use whenever the user wants a PR babysat — triggers include "babysit ci", "babysit do CI", "babysit do PR", "cuida do CI", "olha o CI", "watch the CI", "CI is failing", "CI tá falhando", "verifica o CI do PR", "monitora os comentários do PR", "endereça os comentários que chegarem", or wants failing checks diagnosed and fixed and new review comments addressed as they arrive.
---

## Objective

Take ownership of a given PR until it is merge-ready: poll check status,
diagnose failures from logs, and watch for new review comments — fixing code
issues, re-running flakes or infra failures, addressing reviewer feedback,
and pushing updates — reporting clearly at each step. Stop with a summary
when CI is green and all comments are addressed, or when blocked on something
that needs a human decision.

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

2. **Establish the baseline.**
   - Detect which CI system the PR uses (e.g. `gh pr checks`, `gh run list`,
     or the forge's check API for the PR head sha). Do not assume a specific
     provider — use whatever CLI/API the repository already uses.
   - List all required checks and their current state
     (pending / passing / failing). Report the baseline briefly before
     entering the loop.
   - Snapshot already-seen review comments (ids/timestamps) so the loop only
     reacts to newly arriving ones. Report the count of pre-existing
     unresolved comments without addressing them yet unless the user asked
     for that too.

3. **Enter the watch loop.**
   - Poll check status and new review comments at a sensible interval (a few
     minutes for remote CI; shorter only for fast local-equivalent suites).
     Per Progress reporting above: stay quiet only when nothing changed;
     every transition or new comment gets an immediate update.
   - On each poll with news, report: which checks flipped state since the
     last poll, the current tally (e.g. "3 passing, 1 pending, 1 failing"),
     and any new comments since the last poll (author + what was asked).
   - Keep watching while any required check is pending/queued or new comments
     keep arriving. Move to step 4 as soon as a required check fails, and to
     step 5 as soon as a new comment arrives. Handle one event at a time,
     then re-poll before acting on the next — a fresh push may resolve both
     a failure and a comment thread.

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

5. **Address each new comment.**
   - For every comment that arrived since the last poll, run the
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

6. **Act on the failure classification.**
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

7. **Respect loop safeguards.**
   - Stop after 5 fix-and-push rounds (CI fixes and comment fixes combined)
     or 60 minutes of watching, whichever comes first, and report the current
     state plus what remains.
   - Never push when the working tree has unrelated uncommitted changes —
     ask the user how to proceed instead.
   - Never rebase, retarget, merge, or close the PR unless the user
     explicitly asked for it. Polling and re-running checks never require
     touching the branch.

## Output

- When CI goes green and all arrived comments are addressed: confirm all
  required checks pass on the final sha, list comments addressed (applied /
  replied / declined with reasoning) and fixes pushed, and link the PR.
- When blocked or capped out: report per-check status, the failing step and
  key log lines for each red check, unaddressed comments and what they need,
  what was already tried (re-runs, fixes pushed), and the specific decision
  or action needed from the user.
