---
name: resolve-hunk-comments
description: Resolve review comments left in a live Hunk session. Use whenever the user wants to address Hunk feedback — triggers include "resolver comentários do hunk", "endereça os comentários do hunk", "resolve hunk comments", "aplicar comentários do hunk", "corrigir o que comentei no hunk".
---

## Steps

1. Load the `hunk-review` skill for the CLI conventions (session selection, navigate, comment commands).
2. Discover the live session with `hunk session list --json` before listing comments.
   - If Hunk is visibly open but no sessions are returned, check whether `hunk daemon serve` is running. The TUI can remain usable while its local session broker is absent.
   - If the broker is absent, start `hunk daemon serve` as a long-running process, wait for its API and websocket listeners, then retry `hunk session list --json`. An already-open TUI should reconnect and publish its existing session and notes without being restarted.
   - Only ask the user to reopen Hunk if no session appears after the broker is running. Do not restart the TUI preemptively because user notes may exist only in that process.
3. List the user's own comments: `hunk session comment list --repo . --type user --json`.
   - If there are none, tell the user and stop.
4. For each comment, navigate to it (`hunk session navigate --repo . --file <path> --new-line <n>` or `--old-line <n>`) to read the surrounding code, then load the `resolve-review-comments` skill and run its triage process (classify intent, handle questions, evaluate and act on suggestions). Where that process says "reply" or "record", note it for the final summary instead of posting anywhere.
5. Do not remove or clear comments from the session (`comment rm`/`comment clear`) — leave that to the user, since the comments are their own review notes.
6. When all comments are addressed, use the `commit` skill to commit the changes.

## Output

When all comments are addressed, summarize per comment: what it asked/suggested, what was done (applied / applied with note / needs input), and file:line reference.
