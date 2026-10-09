# AI Exploratory Testing — E2E Flow Testing with Local LLMs — Part A: Hook Script

> **Target Duration:** ~1 minute
> **Purpose:** Hook the viewer, show the high-level workflow, highlight benefits, end with CTA to Part B.
> **When to record:** After Part B is recorded. Use Part B footage for B-roll clips.

---

## Script

> **[HOOK — open with the pain point]**
>
> Your unit tests pass. Your coverage is solid. You deploy. And then someone discovers that your rate limiter returns a 200 instead of a 429 — so clients think rate-limited requests succeeded. Or that your auth middleware checks if an API key *exists* but never validates the *value* — so any string gets through. Or that your RBAC check uses OR instead of AND — so a user with *any one* permission passes a check that requires *all* of them.
>
> These are middleware-level bugs. They live in the space *between* your functions. Unit tests can't see them — they only test functions in isolation. You need to test the full vertical: request → rate limiter → auth → RBAC → view → response. End to end.
>
> **[HIGH-LEVEL WORKFLOW]**
>
> In this video, I'll show you how to use an LLM to do E2E exploratory testing — like fuzzing your middleware stack.
>
> Here's how it works:
> 1. You feed your full Django codebase to an LLM — settings, middleware, views, URL config. Any LLM works — Ollama locally, ChatGPT, Claude, Gemini.
> 2. The AI traces through the complete request lifecycle and generates adversarial curl commands that probe the full middleware chain — not just individual endpoints.
> 3. You run the curls against the live app — this is TDD. You don't assume behavior, you test and capture.
> 4. You feed the actual responses back to the AI. It produces a structured bug report — with flow traces, severity ratings, and fix suggestions.
>
> **[DEMO TEASER]**
>
> In the demo, the AI traces through a Django backend with three middleware layers and catches 7 real E2E flow issues — a rate limiter that only applies to GET requests, an auth check that accepts *any* API key, RBAC logic that lets users through with partial permissions, and a path-matching flaw that bypasses auth entirely. All invisible to unit tests.
>
> **[CTA]**
>
> I'll walk through the full setup — the Django app, both prompt templates, and a live demo. The prompts are LLM-agnostic — no vendor lock-in. Keep watching Part B.

---

## Delivery Notes

- **Tone:** Technical, direct. This is about infrastructure-level bugs, not endpoint testing.
- **Pace:** Quick on the hook (first 15 seconds), then natural rhythm.
- **Emphasis:** The word "between" — these bugs live *between* your functions.
- **Do NOT show:** Setup, commands, or output. That's Part B.
