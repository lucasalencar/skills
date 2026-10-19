---
name: visual-validation
description: Interactively operate the real web or mobile UI from the current PR changes to prove the product works, with screenshots as primary evidence, and produce an agent-authored HTML evidence report. Use whenever the user wants hands-on visual validation — triggers include "validação visual", "validar visualmente", "visual validation", "validate PR visually", "testar visualmente o PR", "evidências visuais", "visual evidence report", or wants screenshots proving the implementation works.
---

# Visual Validation

Operate the product like a user would and prove with screenshots that the PR changes work. Take the current PR (or working-tree) changes, interact with the real interface — web in a browser or mobile in a simulator/emulator/device — exercise the affected flows end to end, and hand back a self-contained HTML report with a pass/fail verdict per scenario and the reason behind it.

This is hands-on product validation, not automated testing. Running unit, integration, or end-to-end test suites (for example `npm test`, `pytest`, `go test`, or CI checks) never counts as visual validation and never replaces interacting with the interface. A scenario passes only when the agent itself operated the UI and captured screenshots showing the product behaving as expected.

The report is always authored directly by the agent executing this skill. Never generate it with a script, generator, template renderer, or scaffold tool. The agent decides the structure, sections, and presentation that best communicate this specific result.

## 1. Resolve the validation scope

1. Honor an explicit PR number, branch, commit range, or working-tree scope supplied by the user.
2. Otherwise, run `gh pr view --json number,title,body,baseRefName,url -q` to detect the open PR. When one exists, the scope is that PR's base through HEAD plus any uncommitted changes on top, and the PR title/description are the stated intent.
3. When no PR exists, compare against `main` when `HEAD` is ahead of it (`main...HEAD` plus uncommitted changes). When that yields nothing meaningful, ask the user for the intended scope instead of guessing.
4. Send a short progress note stating the resolved scope (PR number/URL or range) before doing anything expensive.

Treat the PR description and linked issues/designs as claims about intent, not proof. The validation must prove behavior by observing it.

## 2. Understand what needs visual proof

1. Read the full diff for the resolved scope (`gh pr diff`, `git diff`, `git status` as applicable).
2. Identify every interface surface the change touches, web or mobile: routes/screens, components, navigation flows, gestures and inputs, states (loading/empty/error/success), responsive or device-size behavior, and permissions/roles. For backend-only changes, identify the exact UI path where the effect becomes visible to a user.
3. Trace the code, configuration, migrations, flags, and callers needed to know how to reach each surface as a user and what "working as expected" looks like on screen.
4. Build a validation plan: one concrete hands-on scenario per meaningful behavior, each with entry point in the UI, preconditions/test data, the taps/clicks/typing to perform, and the expected visible outcome on screen. Cover the happy path, the main edge cases the diff introduces, and any regression risk on adjacent screens.
5. If the change genuinely has no reachable interface (pure refactor, internal tooling, docs), say so explicitly and validate through the closest user-operable surface instead. Automated test output is never a substitute: never present test-suite results, coverage, or CI logs as visual evidence.
6. If anything required to operate the product is unknown (environment, seed data, credentials, feature flags, target URL, simulator/device/browser choice), ask the user before starting. Do not invent credentials or test against production without explicit confirmation.

## 3. Prepare a real execution environment

1. Follow repository-local setup instructions (README, AGENTS.md, CONTRIBUTING, package scripts, compose files) over generic guesses.
2. Detect the stack from the repo and start what the scenarios need. For web: dependencies, migrations/seeds, dev servers, tunnels, or preview builds. For mobile: the app build plus a simulator, emulator, or attached device with the build installed, plus any required backend/services.
3. Prefer the project's own commands and keep long-running servers in the background so their logs stay available for the report.
4. Verify the running product serves the code under validation (correct branch/commit, PR preview, or local working tree) and that the interface is actually operable (page loads, app launches) before recording any evidence. If the app does not start or the changed screen is not reachable, stop, report the blocker with logs and a screenshot of the blocking state, and ask how to proceed instead of fabricating results.

## 4. Operate the interface and collect screenshot evidence

Interact with the product as a user for each scenario in the plan. Web means driving a real browser (open the URL, navigate, click, type, submit, resize). Mobile means driving the running app on a simulator, emulator, or device (launch the app, tap, swipe, type, navigate between screens). Code reading, API-only checks, and automated test runs do not satisfy this step.

For each scenario:

1. Perform the scenario's steps through the interface using whatever interactive execution tools are available in this session (browser automation, screenshots, screen recording, simulator/emulator/device control). Show the flow working: reach the changed screen, perform the action, and land on the expected result.
2. Load and follow `references/visual-evidence.md` for every capture. Capture screenshots as the primary, mandatory evidence — at least one per scenario showing the interface in its proving state (result screen, changed component, success/confirmation state), plus before/after or intermediate states whenever they help tell the story. Always capture the full scrollable content top-to-bottom, never just the initially visible viewport. Short clips may supplement but never replace screenshots. Console output, network responses, or server logs are supporting context only.
3. Name every evidence file so its scenario and step are obvious (`01-checkout-happy-path-confirmation.png`, not `screenshot-1.png`). Keep evidence alongside the report or embedded in it; never leave it only in a tool's ephemeral store.
4. Judge each scenario honestly at the time of execution:
   - **Pass** only when you operated the UI yourself and the screenshots show the product behaving as expected end to end.
   - **Fail** when anything deviates on screen, errors, or cannot be exercised (broken flow, wrong data shown, blank/error screen, unreachable surface, environment blocker). Record what was seen on the interface, the exact steps to reproduce it, and the relevant changed location as `path:line`.
5. On failure, capture the failure state as a screenshot plus the error text and logs, and continue with the remaining scenarios unless the environment itself is broken. Never mark a scenario passed on the basis of code reading, automated test output, or reused evidence from a different scenario or run.

## 5. Write the HTML report by hand

Author one responsive, self-contained `.html` file directly — write the markup yourself, in full, as the deliverable. Do not write, run, or reuse a script, CLI, test reporter output, or template engine to produce it. Screenshots and tool-captured artifacts are evidence inputs; the report document itself is hand-written.

Default to a clearly named file in the operating system's temporary directory so the validated repository stays clean; honor a user-specified destination when one is given.

Include whatever sections best tell this validation story, but every report must contain:

- a header identifying the PR/branch/range, commit hash, generation time, and environment (commands run, URLs, browser/device, seed data);
- a summary with total passed/failed/blocked counts and one line per scenario linking to its detail;
- one section per scenario with: status (pass/fail/blocked), expected vs. observed behavior on the interface, the reason for the verdict, numbered UI reproduction steps, embedded screenshots proving the verdict (images viewable without external hosts), and links to the narrow changed locations or PR Files-changed view when available;
- a failures section (or an explicit "no failures" statement) explaining each failure's cause or best-supported hypothesis, with logs and error text;
- limitations and follow-ups: anything not exercised, assumed, or needing human judgment.

Design for standalone reading:

- embed CSS and evidence so the page stays complete if scripts or network resources fail; prefer embedded images (or a sidecar `assets/` folder next to the report when embedding would make the file unwieldy — in that case keep paths relative and verify they resolve);
- keep typography, color, and status badges restrained and consistent; pass/fail must be scannable and never color-only (always pair with text labels);
- code, paths, and logs wrap or scroll without breaking layout; include print styles and semantic headings, sufficient contrast, text equivalents for images, and reduced-motion behavior.

Open the finished file with the platform's normal browser-opening mechanism. If the environment requires authorization for opening a local file, request it at that point.

## 6. Finish in chat

In chat, return only a concise completion note: scope validated, counts (X passed / Y failed / Z blocked), one line per failure with its cause, the report file path, and anything the user must decide next. The full evidence and reasoning live in the HTML report, not in chat.

## Completion criteria

Before opening the report, verify that:

- the validated scope matches the resolved PR/range and the code actually executed;
- every scenario has a verdict backed by fresh screenshots of the real interface captured while operating it during this run, with full top-to-bottom coverage of every scrolled surface — no verdict by inference, no automated-test output presented as visual proof, no reused or placeholder images, no proving content cut off by the viewport edge;
- every failure or blocked scenario states what broke, how to reproduce it, and where in the code it points;
- the HTML was written directly by the agent (no generator script in the workflow), opens locally, reads well at narrow and wide widths, and keeps images and styles intact with no network dependency;
- limitations, assumptions, and untested surfaces are stated rather than silently omitted.
