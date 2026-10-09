# AI-Powered PR Code Review (Ollama — Free, Local) — Screen Recording Guide

> **Purpose:** Video split plan, recording settings, cue sheet, and checklist for the screen recording session.

---

## VIDEO SPLITS

Record in these 5 logical segments. Each is a self-contained video file.

| # | Video Name | Part B Steps | What to Show | Est. Duration |
|---|-----------|-------------|--------------|---------------|
| 1 | **Setup: Ollama + Model** | B0.1 – B0.3 | Install Ollama, pull qwen2.5-coder:7b, run the sanity check | 5-7 min |
| 2 | **Project: HTTP Retry Handler** | B1.1 – B1.3 | Create repo, write placeholder on main, create feature branch with retry code that has hidden edge cases | 5-8 min |
| 3 | **Script: ai-review.sh** | B2.1 – B2.3 | Write the review script, make executable, walk through the prompt line by line | 5-7 min |
| 4 | **Demo: AI Catches Edge Cases** | B3.1 – Step 4 | Run `./ai-review.sh main`, wait for output, walk through each finding | 8-12 min |
| 5 | **Fix + PR** | B5.1 – Closing | Apply all fixes, re-run review (clean pass), push, open PR, closing recap | 5-8 min |

**Total estimated recording time:** 28-42 min raw footage

---

## RECORDING SETTINGS

| Setting | Value |
|---------|-------|
| **Theme** | Light theme on everything — IDE, terminal, browser, GitHub |
| **Font size (IDE)** | 14-16pt (readable on 1080p) |
| **Font size (terminal)** | 14-16pt |
| **Terminal** | Use a clean terminal with minimal prompt (no long paths or git decorations) |
| **Resolution** | 1920×1080 or higher |
| **Speed** | Normal speed throughout — NO fast-forwarding, NO time-lapses |
| **Cropping** | Do NOT crop or trim before uploading raw footage |
| **Notifications** | Turn OFF system notifications, Slack, email popups before recording |
| **Tabs** | Close unrelated browser tabs and IDE files |

---

## CUE SHEET — What to Say and When

### Video 1: Setup

| Timestamp (approx) | Cue |
|-------------------|-----|
| Start | *"Let's set up the tools. We need two things: Ollama to run the LLM locally, and a code-optimized model."* |
| After `ollama serve` | *"Ollama runs LLMs entirely on your machine. No account, no API key, no cloud. Your code stays on your laptop."* |
| After `ollama pull` | *"I'm using qwen2.5-coder 7B — optimized for code, fits on most laptops. Alternatives on screen if you have more RAM."* |
| After sanity check | *"The model understands code and gives real feedback. We're ready."* |

### Video 2: Project Setup

| Timestamp (approx) | Cue |
|-------------------|-----|
| Creating feature branch | *"I'm writing an HTTP retry handler — exponential backoff, configurable retries, proper exception handling."* |
| After writing the code | *"This looks clean. It works — if you test it against a server that returns 500 then 200, it retries and succeeds. This is exactly what Cursor or Copilot would generate."* |
| Before committing | *"But this code has 3 missing edge cases that will cause real problems in production. I'm NOT going to tell you what they are — let's see if the AI catches them."* |

### Video 3: Review Script

| Timestamp (approx) | Cue |
|-------------------|-----|
| Writing the script | *"Three moving parts: git diff to extract changes, a structured prompt, and ollama run to pipe it to the local model."* |
| Walking through prompt | *"Notice the prompt is tuned for production-readiness, not just syntax. It asks about HTTP protocol violations, unbounded delays, edge cases that pass testing but fail in production."* |
| After chmod +x | *"This script works on any repo, any language. Copy it into any project and run it."* |

### Video 4: The Demo 🎬

| Timestamp (approx) | Cue |
|-------------------|-----|
| Running `./ai-review.sh` | *"One command. Let's see what it finds."* |
| While waiting | *"The model is analyzing our diff locally. No cost, no API key, no code leaving the machine. A few extra seconds is the trade-off for running local."* |
| **Output appears** | **🎬 "This is the wow factor. Let's go through what the AI found."** |
| Edge Case 1 (retries all errors) | *"It caught that we're retrying ALL errors — including 401 Unauthorized and 404 Not Found. Retrying a 401 is pointless. We should only retry server errors and rate limits."* |
| Edge Case 2 (Retry-After) | *"It caught that we're ignoring the Retry-After header on 429 responses. When a server says 'wait 30 seconds,' you wait 30 seconds. Ignoring this can get you IP-banned."* |
| Edge Case 3 (no max delay) | *"It flagged unbounded backoff. With high retry counts, later attempts could wait minutes."* |
| Edge Case 4 (narrow except) | *"And it caught that we only handle HTTPError, not ConnectionError or Timeout — the most common transient network failures."* |
| **Key point** | **"This is EXACTLY the code Cursor or Copilot would generate. It looks correct, passes tests. But the AI coding assistant helped you WRITE the code — it didn't REVIEW it for production-readiness. That's the gap this fills."** |
| Closing | *"And all of this ran locally. Our code never left this machine."* |

### Video 5: Fix + PR

| Timestamp (approx) | Cue |
|-------------------|-----|
| Applying fixes | *"Four fixes: retryable status code filtering, Retry-After header support, max delay cap, broader exception handling."* |
| Clean re-run | *"Clean pass. All edge cases addressed."* |
| Opening PR | *"I'm including the AI findings in the PR description so the reviewer knows what was already caught. They focus on architecture and design."* |
| **Closing recap** | See the full closing script in Part B, Step "Closing Recap" |

---

## PRE-RECORDING CHECKLIST

- [ ] Ollama installed and `ollama serve` running
- [ ] `qwen2.5-coder:7b` pulled and verified with `ollama list`
- [ ] Light theme set on IDE, terminal, and browser
- [ ] Font sizes bumped to 14-16pt
- [ ] System notifications OFF
- [ ] Unrelated tabs and files closed
- [ ] Screen recording tool ready (OBS, QuickTime, or similar)
- [ ] Microphone tested — clear audio, no background noise
- [ ] This cue sheet open on a second monitor or printed

## POST-RECORDING CHECKLIST

- [ ] All 5 videos saved with correct names
- [ ] No accidental API keys, passwords, or sensitive data visible in recordings
- [ ] Review each video once for audio clarity
- [ ] Upload raw footage — do NOT crop or trim
- [ ] Update Part B script if you discovered anything different during recording

---

## KEY PHRASES TO REPEAT

Mention each of these at least once across the 5 videos:

| Phrase | When to say it |
|--------|---------------|
| *"No API keys, no cloud, no cost"* | Videos 1, 4, and 5 |
| *"Code never leaves your machine"* | Videos 1 and 4 |
| *"This is exactly what Cursor/Copilot would generate"* | Video 4 |
| *"AI helped you WRITE the code — this REVIEWS it"* | Video 4 |
| *"Works on any repo, any language"* | Videos 3 and 5 |
| *"This is the wow factor"* | Video 4 (when output appears) |
