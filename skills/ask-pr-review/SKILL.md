---
name: ask-pr-review
description: Request a Pull Request review. Runs a fixed baseline (improve description, mark ready) then executes team-specific custom steps from memory. Learns each team's workflow on first use and supports multiple repos per team.
---

# Requirements

- GitHub CLI (`gh`) authenticated
- Additional tools (Slack MCP, Atlassian MCP, etc.) only if the team's custom steps require them

# Step 1 — Identify the team and load custom steps

## 1.1 Load saved configurations

Check if `~/.claude/pr-review-preferences.md` exists and read it. The file contains team configurations in YAML inside a code block.

## 1.2 Detect the current team

Run `gh repo view --json nameWithOwner -q .nameWithOwner` to get the current repository.

Match the repo against each team's `detect_by_repos` list (exact or substring match on any entry):
- One match → use it silently
- Multiple matches → ask the user which team applies
- No match → go to step 1.3

## 1.3 Onboard: new repo, unknown team

No configured team matched the current repo. Before starting from scratch, check if there are already saved teams.

**If saved teams exist**, present them to the user:

> "I don't have a configuration for `<repo>` yet. Does it belong to one of these teams, or is it a new one?"
> _(list team names)_
> "Or: new team"

- **Existing team chosen** → add the current repo to that team's `detect_by_repos` list and save. Skip to Step 2.
- **New team chosen** → continue below.

**If no saved teams exist**, or the user chose "new team":

Ask the user two things:

1. "What should I call this team? (e.g. `Smith`, `Side Project`)"

2. "Describe step by step what you want me to do when requesting a review for this team. Include everything: which Slack channel to post to and in what format, whether to move a Jira card and from/to which status, whether to add a comment, assign someone, or anything else."

### Validate and enrich the described steps

Before saving, extract every external resource mentioned in the description and validate each one via MCP. The goal is to save resolved, specific identifiers — not the user's raw words.

**Slack channels:**
- For each channel name mentioned (e.g. `#smith-eng-prs`), search Slack MCP using `slack_search_channels`.
- If exactly one match is found, confirm with the user: "Found `#smith-eng-prs` (ID: `C0123ABCD`). Is this the right channel?" and replace the channel reference in the steps with the confirmed name and ID.
- If multiple matches are found, list them and ask the user to pick one.
- If no match is found, tell the user and ask them to double-check the name.

**Jira projects and statuses:**
- For each Jira project key or board mentioned (e.g. `SMITH`, `In Progress → In Review`), use the Atlassian MCP to verify the project exists (`getVisibleJiraProjects` or `searchJiraIssuesUsingJql` with `project = <key>`).
- If the project exists, fetch the available workflow statuses for that project and confirm that the `from` and `to` status names match exactly. If the user's names are ambiguous (e.g. `"In Progress"` vs `"In Development"`), show the actual status names and ask which ones apply.
- Replace status names in the steps with the exact names returned by Jira.

**Only proceed to save after all validations pass.** If any resource cannot be confirmed, loop back and ask the user to correct it before saving.

### Rewrite the steps for LLM execution

Once all resources are validated, rewrite the custom steps from scratch as a numbered list of clear, unambiguous instructions. Do not save the user's raw description. The rewritten steps must:

- Use exact identifiers resolved during validation (Slack channel name + ID, exact Jira status names, project key)
- Describe the action clearly without naming specific tools or commands — focus on what needs to happen, not how (e.g. "Post to Slack channel `#smith-eng-prs` (C0123ABCD)")
- Include the exact message format when posting to Slack, with placeholder tokens like `<PR link>` and `<PR title>`
- Be self-contained — a future LLM reading only these steps should be able to execute them without ambiguity or guesswork

Show the rewritten steps to the user and ask for confirmation before saving: "Here's how I'll document these steps. Does this look right?"

Save to `~/.claude/pr-review-preferences.md`, preserving existing teams. Use this format:

~~~markdown
# PR Review Preferences

```yaml
teams:
  - name: "Team Name"
    detect_by_repos:
      - "org/repo-name"
    custom_steps: |
      <exactly what the user described, verbatim>
```
~~~

Confirm: "Got it. I'll follow these steps every time you request a review on this repo."

---

# Step 2 — Find the Pull Request

Use current context (branch name, recent commits, `gh pr list`) to infer the PR. If ambiguous, ask the user.

---

# Step 3 — Baseline: review and improve the PR title and description

1. Read the PR diff, title, and description via `gh pr view --json body,title,files`.
2. Check the **title**: it should reflect the final scope of the changes, not the original intent when the branch was created. If it's stale or misleading, propose an updated title. **Do not update without user approval.**
3. Check the **description**: it should accurately cover all meaningful changes. If it needs improvement, propose an updated version and explain what changed. **Do not update without user approval.**
4. Apply approved changes: `gh pr edit <number> --title "<title>" --body "<description>"`. If only one changed, update only that field.

---

# Step 4 — Baseline: mark as ready for review

If the PR is a draft: `gh pr ready <number>`. Otherwise skip.

---

# Step 5 — Execute team custom steps

Read the `custom_steps` field from the team configuration loaded in Step 1.

Execute each instruction described there, in order. Treat the custom steps as direct instructions — follow them exactly as written, using whatever tools are needed (Slack MCP, Atlassian MCP, `gh` CLI, etc.).

If a step is ambiguous or missing required information (e.g. a ticket key that can't be inferred), ask the user before proceeding.

---

# Output

Summarize what was done in 2–3 lines. Include any relevant links (PR, Slack message, Jira ticket).
