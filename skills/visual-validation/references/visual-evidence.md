# Visual Evidence

How to capture screenshots that actually prove the product works. Load and follow this file whenever collecting evidence.

## Capture the whole content, not just the viewport

- A single viewport screenshot is almost never sufficient. Scrollable pages, lists, tables, drawers, and modals routinely hide the validated information below the fold.
- For every proving state, capture the full scrollable extent: scroll from top to bottom through each scroll container and capture overlapping screenshots so no section is missing. Prefer a full-page capture when the tooling supports it; otherwise stitch the sequence manually in the report in top-to-bottom order.
- Treat every scroll container independently: the page, plus nested scrollers (tables with horizontal scroll, sidebars, modal bodies, mobile scroll views). Scroll each one to its end and capture its content.
- Overlap consecutive captures slightly so the reader can follow continuity. Never skip the middle of a long page to save time.
- For horizontally scrolling content (wide tables, carousels), scroll sideways to the far edge as well and capture the hidden columns/items.

## Prove the outcome is visible and legible

- Before marking pass, open each screenshot and confirm the validated information is actually visible and readable in the image: values, names, statuses, totals, error messages. If you cannot read it in the evidence, it does not count as proof — recapture.
- Wait for loading to finish (skeletons, spinners, lazy images) before capturing. Evidence showing a loading state proves nothing about the final result.
- Use realistic data where possible so the screenshot demonstrates the behavior (e.g. a created record appearing in a list, a total updating), not an empty state that could hide a bug.
- Capture the interaction and its result together when the story needs it: the filled form plus the confirmation, the action plus the updated state. One isolated screen that could predate the action is weak evidence.

## Keep context attached

- Each screenshot must be attributable: scenario, step number, URL/route or screen name, viewport or device, and scroll position when relevant. Encode this in the file name and the report caption (`02-orders-list-after-create-fullpage.png`, not `screenshot-2.png`).
- Include just enough surrounding context (route, tab, selected row) that a reviewer can tell where in the product the capture was taken. Crop out nothing that identifies location or state.
- Record the environment once per report (browser/device, viewport size, simulator model, seed data) instead of repeating it per image, but flag any capture taken under different conditions.

## Web specifics

- Capture at a realistic desktop viewport first, then re-check breakpoints the diff touches (narrow/mobile widths) when layout or visibility is in question.
- Expand collapsed sections, tabs, accordions, and tooltips that hold validated content, and capture them open.
- For sticky headers/footers, note that full-page captures may repeat them; prefer one full-page capture plus one viewport capture showing the natural on-screen appearance.

## Mobile specifics

- Capture the full scroll view top-to-bottom, including content reachable only by scrolling. Dismiss the keyboard before capturing a form result so it does not cover the proving content, then capture the result state separately.
- Capture on the simulator/emulator/device the change targets; note the model, OS version, and orientation. Re-capture in the other orientation only when the diff affects layout.

## Failure and blocked evidence

- On failure, capture the failing state in full (whole screen plus scrolled content), the exact error text legibly, and the steps that led there. Add console, network, or server logs as supporting context — never as a replacement for the screenshot.
- When the interface cannot be reached at all, capture the blocking state (blank page, crash, error screen) as the evidence and mark the scenario blocked, not passed.

## Self-check before writing the report

- Every scenario has at least one screenshot showing its proving state in full, with no validated content cut off by the viewport edge.
- Every long or scrollable surface has top-to-bottom coverage with no skipped middle.
- Every image is legible, attributable, and stored alongside or embedded in the report — nothing lives only in a tool's ephemeral store.
