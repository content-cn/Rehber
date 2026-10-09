# AI-Powered PR Code Review (Ollama — Free, Local) — Part A: Hook Script

> **Target Duration:** ~1 minute
> **Purpose:** Hook the viewer, show the high-level workflow, highlight benefits, end with CTA to Part B.
> **When to record:** After Part B is recorded. Use Part B footage for any B-roll clips.

---

## Script

> **[HOOK — open with the pain point]**
>
> You write an HTTP retry handler. It looks clean. It passes your tests. Your reviewer approves it. And three weeks later, your service gets IP-banned in production because your code was blindly retrying rate-limited requests without reading the Retry-After header. The bug was right there in the diff — nobody caught it.
>
> **[HIGH-LEVEL WORKFLOW]**
>
> What if every PR got an instant first-pass review — in seconds, not hours — before a human ever looked at it?
>
> In this video, I'll show you how to build a one-command AI code reviewer using Ollama and a simple shell script. No API keys. No cloud. No cost. Your code never leaves your machine.
>
> Here's how it works:
> 1. You write your code on a feature branch — just like normal.
> 2. Before pushing, you run one command: `./ai-review.sh main`
> 3. The script extracts your git diff and feeds it to a coding LLM running locally on Ollama.
> 4. The AI analyzes the diff like a pedantic senior engineer — not just looking for syntax errors, but reasoning about production behavior: missing edge cases, protocol violations, unhandled error paths.
> 5. You fix what it finds, then push for human review. The human reviewer focuses on architecture and design — the edge-case hunting is already done.
>
> **[DEMO TEASER]**
>
> In the demo, I'll show the AI catching 3 missing edge cases in an HTTP retry handler — the exact kind of code that Cursor or Copilot would generate without flagging any issues. It passes all happy-path tests. But the AI reviewer catches that it retries non-retryable errors like 401s, ignores the Retry-After header on 429s, and has no cap on backoff delays. These are production failures waiting to happen — and the AI flags all three in seconds.
>
> **[CTA]**
>
> I'll walk through the full setup step by step — Ollama install, the exact review prompt, the shell script, and a live demo with a real PR. Keep watching Part B.

---

## Delivery Notes

- **Tone:** Confident, conversational, not salesy. You're showing a fellow developer something useful.
- **Pace:** Steady — not rushed. The hook (first 10 seconds) should be slightly faster to grab attention, then settle into a natural pace.
- **Visuals (if adding B-roll):** Show the terminal output from Part B's Step 4 briefly during the demo teaser.
- **Do NOT show:** Detailed setup, commands, or code. That's all Part B.
