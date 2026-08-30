---
name: pr-comment-writing
description: Define style for Pull Request review comments and replies (tone, concision, AI disclosure). Use whenever drafting or posting a PR comment or reply — triggers include "escrever comentário de PR", "responder comentário do PR", "review comment", "PR comment style", or before any skill that posts PR comments (add-pr-comments, resolve-pr-comments).
---

# Pull Request comment writing

## Language

- For a new review comment, write in the language used by the PR title and description. Obtain them with `gh pr view --json title,body`.
- For a reply in an existing thread, write in the language of the comment being answered. Default to English.

## New review comments

Use one of two collaborative tones, choosing the one that fits the review point:

1. **Genuine question:** Ask directly when the author's context or reasoning is needed, or when multiple approaches are plausible. For example: "Why did you choose X here?", "Could this cause Z?", or "Would Y also need to change when this value changes?"
2. **Direct suggestion:** When the issue and practical improvement are clear, state the problem and recommendation plainly: observation → consequence → recommended action → invitation to engage. Make the invitation specific to the suggestion, for example: "This duplicates the validation logic in `src/validators/user.ts`, so the two paths can drift. Could we extract it into a shared helper?"

Vary the final invitation. Do not repeatedly use "What do you think?". Prefer a closing that follows naturally from the recommendation, such as "Could we…?", "Would it make sense to…?", "Would you be open to…?", "Does that fit the intended…?", or "How does that sound?".

Do not turn a clear recommendation into an indirect question just for politeness. Conversely, do not present an uncertain concern as a directive: ask a genuine question when the author's intent or missing context matters. Avoid judgmental phrasing such as "this is wrong".

## AI disclosure

Append a short signature to every posted new review comment and reply disclosing that it was AI-generated, naming the active client and model, for example: `— comment generated with <client> (<complete model name>)`.

## Replies

Keep replies concise: answer the specific question or point raised, nothing more. Reference a file or code snippet only when needed to make the reply clear.
