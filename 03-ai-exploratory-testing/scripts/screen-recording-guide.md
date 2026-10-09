# AI Exploratory Testing — E2E Flow Testing — Screen Recording Guide

---

## VIDEO SPLITS

| # | Video | Part B Steps | What to Show | Est. Duration |
|---|-------|-------------|--------------|---------------|
| 1 | **Setup: Ollama + Django App** | B0.1–B0.3 | Install Ollama, pull 16B model, start Django app, health check | 5-7 min |
| 2 | **Codebase Walkthrough** | B1.1–B1.5 | Walk through settings, middleware stack, auth, views, URLs. Don't reveal bugs. | 5-7 min |
| 3 | **AI Generates E2E Scenarios** | B2.1–B2.5 | Feed codebase to LLM, show flow traces and curl generation | 10-15 min |
| 4 | **Run Curls — TDD** | B3.1–B3.7 | Execute curls live, capture actual responses, show each failure | 10-15 min |
| 5 | **AI Bug Report** | B4.1–B4.3 | Feed results back, walk through bug report with middleware health | 8-12 min |
| 6 | **Fix + Verify + Recap** | B5.1–Closing | Apply fixes, re-run scenarios, closing recap | 5-8 min |

**Total:** 43-64 min raw

---

## RECORDING SETTINGS

| Setting | Value |
|---------|-------|
| **Theme** | Light — IDE, terminal, browser |
| **Font size** | 14-16pt (IDE + terminal) |
| **Terminal** | 2 terminals: one running Django server, one for curls |
| **Resolution** | 1920×1080+ |
| **Speed** | Normal — no fast-forwarding |
| **Notifications** | OFF |

---

## CUE SHEET

### Video 1: Setup
| When | Say |
|------|-----|
| Start | *"We need an LLM and a Django backend to test. I'm using Ollama locally but the prompts work with any LLM."* |
| After model pull | *"deepseek-coder-v2 16B. For E2E flow analysis across middleware, you need at least 16B parameters."* |
| After health check | *"The app works. 9 endpoints, 3 middleware layers. Let's trace the full flow."* |

### Video 2: Codebase Walkthrough
| When | Say |
|------|-----|
| Showing MIDDLEWARE list | *"Three layers: logger, rate limiter, auth. Every request goes through all three. Order matters."* |
| Showing auth.py | *"Three tiers: public skip auth, internal need API key, everything else needs Bearer + RBAC."* |
| Before closing | *"Let's NOT look for bugs ourselves. Let's feed this to the AI and see what it traces."* |

### Video 3: AI Generates Scenarios 🎬
| When | Say |
|------|-----|
| Showing prompt | *"This asks the AI to trace the COMPLETE request lifecycle. Like fuzzing the E2E flow. Works in any LLM."* |
| While waiting | *"It's reading middleware, auth logic, URL config — tracing request paths across the full stack."* |
| **Output appears** | **🎬 "Look at the flow traces. The AI traced: Request → Logger → RateLimiter SKIPPED because method is POST → Auth → View. It found the gap in the middleware chain."** |
| RBAC scenario | *"It walked through _check_permissions() and identified that set intersection is OR logic, not AND."* |
| Key point | *"These prompts are LLM-agnostic. Same text works in ChatGPT, Claude, Gemini. No vendor lock-in."* |

### Video 4: Running Curls — TDD 🎬
| When | Say |
|------|-----|
| Start | *"TDD approach. We don't assume. We test and capture."* |
| Rate limiter 200 | *"200 OK. The rate limiter blocked us but returned success. Wrong rejection policy."* |
| POST bypass | *"150 POST requests, zero throttling. Rate limiter only checks GET."* |
| Any API key works | *"Any string as an API key. Auth checks existence, not value. And it leaks config."* |
| RBAC bypass | *"Bob lacks write:orders but gets through. OR logic instead of AND."* |

### Video 5: Bug Report 🎬
| When | Say |
|------|-----|
| **Report appears** | **🎬 "7 bugs, 3 critical. Full middleware health report. And backwards compatibility notes."** |
| Middleware health | *"Request Logger: clean. Rate Limiter: 3 issues. Auth: 4 issues."* |
| Key point | *"Unit tests would test each function alone. They'd never find these — you need to trace the full flow."* |
| Regression angle | *"Save these scenarios. Re-run before every release. That's your regression check."* |

### Video 6: Fix + Recap
| When | Say |
|------|-----|
| Applying fixes | *"Six fixes across two middleware files."* |
| Clean re-runs | *"429 on rate limit. 401 on bad key. 403 on insufficient permissions. Fixed."* |
| **Closing** | See Part B "Closing Recap" |

---

## PRE-RECORDING CHECKLIST

- [ ] Ollama installed, `deepseek-coder-v2:16b` pulled
- [ ] Django app starts: `python manage.py runserver 8000`
- [ ] Health check works: `curl http://localhost:8000/api/health`
- [ ] Prompt templates in `prompts/` directory
- [ ] Light theme, 14-16pt fonts
- [ ] Notifications OFF, unrelated tabs closed
- [ ] Two terminals ready
- [ ] Mic tested, recording tool ready
- [ ] This cue sheet on second monitor

## POST-RECORDING CHECKLIST

- [ ] 6 videos saved
- [ ] No secrets/keys visible in footage
- [ ] Audio clear
- [ ] Upload raw — no trimming

---

## KEY PHRASES TO REPEAT

| Phrase | When |
|--------|------|
| *"E2E flow testing — like fuzzing the middleware stack"* | Videos 2, 3 |
| *"Unit tests can't see this — they test functions in isolation"* | Videos 3, 5 |
| *"LLM agnostic — works with any model, no vendor lock-in"* | Videos 1, 3, 6 |
| *"TDD — test and capture, don't assume"* | Video 4 |
| *"This is the wow factor"* | Videos 3, 5 |
| *"Reduces manual regression testing between releases"* | Videos 5, 6 |
| *"Fewer bugs, faster releases, reduced testing time"* | Video 6 |
| *"Proves business logic is intact end-to-end"* | Video 6 |
| *"Backwards compatibility — AI flags which fixes could break clients"* | Video 5 |

---

## FLOW DIAGRAM (on-screen graphic)

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Full Codebase│────▶│ Prompt 1     │────▶│ 15 E2E Test  │────▶│ Run curls    │
│ (7 files)    │     │ (Any LLM)    │     │ Scenarios    │     │ against live │
└──────────────┘     └──────────────┘     │ + Flow Traces│     │ app (TDD)    │
                                          └──────────────┘     └──────┬───────┘
                                                                      │
                    ┌──────────────┐     ┌──────────────┐     ┌───────▼──────┐
                    │ Fix + verify │◀────│ Bug Report   │◀────│ Prompt 2     │
                    │ re-run       │     │ + Middleware  │     │ (Any LLM)    │
                    └──────────────┘     │   Health     │     └──────────────┘
                                         └──────────────┘
```
