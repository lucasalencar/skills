---
name: prepare-for-review
description: Guarantee a Pull Request is actually healthy before it is announced as ready for review. Use whenever the user wants to leave a PR ready — triggers include "deixar o PR pronto", "garantir que o PR está pronto", "preparar o PR", "prepare the PR", "ensure the PR is ready", "get CI green", "atualizar a branch do PR", or before requesting a review. Pushes local changes, brings the branch current with its base, and waits for CI to go green in a single pass ending when healthy or blocked.
---

## Objective

Run a one-time health gate on the target PR: push pending changes, bring
the branch current with its base branch when that rebases cleanly, and get
required CI green on the current head SHA. This is a single pass, not a
persistent watch — it ends as soon as the PR is healthy (CI green, branch
current, no conflicts) or blocked (failure outside PR scope, conflicting
rebase, ambiguous decision).

This skill never announces the PR as ready and never monitors it
long-term. Announcing (title/description updates, marking ready, notifying
reviewers) and continued observation while the team reviews are out of
scope — separate steps the user takes afterwards.

This gate is an auto-push workflow for changes it creates. After every fix
commit or clean rebase, push automatically as part of that action; do not
pause to ask whether to push. Keep commits atomic with clear messages and
run available fast validation before pushing.

## Steps

1. **Resolve the target PR.**
   - Use a PR number/URL supplied by the invoking workflow; otherwise use the
     PR associated with the current branch.
   - If there is no open PR for the branch and the user expected one, stop
     and say so instead of guessing.
   - Record the PR head branch and sha; if the sha changes mid-gate (new
     push), restart evaluation against the new sha.
   - Verify the PR base branch (default `main`). If it targets another
     branch, report that fact and ask whether that branch should replace
     `main` as the update source; do not silently rebase onto a different
     target.

2. **Push local changes.**
   - Commit pending changes for this PR in atomic commits with clear
     messages, run available fast validation (lint, typecheck, or tests on
     touched files), then push.
   - Never push when the working tree has unrelated uncommitted changes —
     ask the user how to proceed instead.

3. **Bring the branch current safely (clean rebase only).**
   - Check whether the branch is behind its base (`gh pr view --json
     baseRefName,headRefOid` plus `git fetch` + behind-count against the
     base).
   - When behind, fetch the base and preflight whether the PR commits apply
     cleanly onto it (for example, `git merge-tree --write-tree HEAD
     <remote>/<base>`).
   - Only when the preflight is clean, announce the exact base SHA, rebase
     onto it, verify the resulting branch, and push with
     `--force-with-lease`. Re-check that the remote head is still the SHA
     evaluated before rebasing; if it changed, abandon the attempt and
     re-evaluate.
   - If the preflight reports conflicts, leave the branch untouched, report
     the conflicting paths, and end the gate as blocked — never
     auto-resolve conflicts.

4. **Wait for CI once and handle the result.**
   - Detect which CI system the PR uses (e.g. `gh pr checks`, `gh run list`,
     or the forge's check API for the PR head sha). List required checks and
     their state (pending / passing / failing).
   - Poll at a sensible interval (a few minutes for remote CI) until the
     required checks on the current head SHA complete. This single wait ends
     on green or on failure; it does not persist afterwards.
   - On failure, fetch only the failing logs (e.g. `gh run view
     --log-failed`) and classify before acting:
     - **Flake / infra**: timeout, runner lost, network/DNS blip, rate
       limit, out-of-disk, service unavailable, or a test that passes on
       retry without code changes → re-run only the failed jobs/checks
       (never the full matrix unless the provider lacks per-job rerun).
       Cap blind re-runs at 2 per check — a third identical failure is
       treated as a real failure.
     - **Code issue in this PR**: test failure, lint/type error, or build
       break caused by the PR's own changes → fix in scope, verify with the
       narrowest local reproduction available, then commit and push, and
       wait for CI on the new SHA once.
     - **Broken base / external** or **needs human decision**: failure on
       files the PR did not touch, upstream breakage, expired
       secrets/tokens, policy sign-off, or a fix that would expand scope →
       end the gate as blocked and report; do not push speculative fixes.
   - State the classification and the evidence (failing step, error lines)
     before acting — never push or re-run before announcing it.

5. **End the gate.**
   - The gate passes when required CI is green on the current head SHA, the
     branch is current with its base, and there are no merge conflicts.
   - End as blocked when CI is red outside PR scope, the rebase conflicts,
     or a human decision is needed. Report per-check status, the failing
     step and key log lines for each red check, conflicting paths, what was
     already tried (re-runs, fixes pushed), and the specific decision or
     action needed from the user.
   - Never retarget, merge, close, or announce the PR.

## Output

- When healthy: confirm the final PR SHA and base SHA, per-check status
  (green), that the branch is current and conflict-free, and every fix,
  re-run, or rebase pushed. Link the PR and state it is ready to be
  announced.
- When blocked: report per-check status, failing step + key log lines,
  conflicting paths, what was tried, and what is needed from the user. Do
  not announce the PR.
