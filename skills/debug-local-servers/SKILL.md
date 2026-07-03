---
name: debug-local-servers
description: Investigate what's happening with local dev servers running in tmux panes by pulling their stdout logs. Use when the user is debugging a local setup where multiple servers run in a tmux window/session and wants help understanding an error, unexpected behavior, or test failure from their logs.
---

# Debug Local Servers

The user runs several local servers side by side in tmux panes within one window,
each streaming its logs to stdout. When something breaks, the fastest way to
understand it is to pull those logs directly instead of guessing.

## Workflow

1. **Locate the tmux window with the servers.**
   - If the user already named the session/window in this conversation, use it.
   - Otherwise ask which tmux session and window has the servers running. Accept
     a session name, window name/index, or "the one I'm in" (see terminology
     note below).
   - Use `mcp__tmux__list-sessions` / `mcp__tmux__find-session` and
     `mcp__tmux__list-windows` to resolve it if the user gives a name instead of
     an ID.

2. **Enumerate the panes.**
   - Use `mcp__tmux__list-panes` on that window to get every pane ID.
   - If there are multiple panes, try to identify which server/process runs in
     each (pane title, or the first lines captured) so logs can be attributed
     correctly in the summary.

3. **Capture logs from each pane.**
   - Use `mcp__tmux__capture-pane` per pane. Default to a few hundred lines;
     pull more if the user is chasing something further back in history, or
     less if they only care about the latest request/error.
   - Prefer capturing from all panes in the window rather than guessing which
     one is relevant — cross-service issues often show up in a pane other than
     the one the user suspects.

4. **Summarize before diving in.**
   - Briefly state which servers/panes were found and anything that stands out
     (errors, stack traces, restarts) before proposing next steps or asking
     clarifying questions.

5. **Continue the investigation normally** using this captured context —
   correlate errors across services, check timestamps, grep for a request ID,
   etc. — as the conversation requires.

## Notes

- "janela"/"window" and "painel"/"pane" refer to tmux windows/panes.
- Only capture panes in the window the user pointed to; don't sweep every tmux
  session unless asked.
- If a pane's visible scrollback isn't enough (e.g. the error is way back or
  the server logs to a file instead of stdout), ask the user or check for a log
  file before giving up.
