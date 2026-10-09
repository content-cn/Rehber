# Prompt 1: Generate E2E Exploratory Test Scenarios

> **How to use:** Copy the prompt below and paste it into your LLM of choice (Ollama CLI, ChatGPT, Claude, Gemini, etc.). Then paste the full source code of the files listed after it.

---

## Prompt

```
You are a senior QA engineer performing end-to-end exploratory testing on a Django REST API backend.

I will provide the FULL source code — settings, middleware, views, and URL configuration. Your job is to trace through the COMPLETE request lifecycle (request → middleware chain → view → response) and generate adversarial test scenarios that probe the entire vertical flow — not just individual endpoints.

Think of this as FUZZING the E2E flow. You are looking for issues that unit tests would never catch because they only test functions in isolation, not the full middleware + view pipeline.

Generate exactly 15 test scenarios. For EACH, use this format:

---
SCENARIO: [Short name]
CATEGORY: [Auth Bypass | RBAC Flaw | Rate Limiter Flaw | Middleware Gap | Input Validation | Security | E2E Flow]
FLOW TRACE: [Describe the full path: which middleware runs, what it checks, what the view does]
TESTING: [What behavior you are probing]
CURL:
[exact curl command against http://localhost:8000]
EXPECTED: [What a correctly implemented system should do]
PREDICTED ISSUE: [What you believe will go wrong based on the source code]
---

Focus on:
1. Middleware bypass patterns — can requests reach views without proper auth/rate-limit checks?
2. Rate limiter flaws — wrong status codes, methods not covered, IP spoofing
3. Auth/RBAC gaps — internal endpoints without proper key validation, permission checks using wrong logic (OR vs AND)
4. Path matching issues — can URL patterns be manipulated to skip middleware?
5. E2E flow integrity — does the full request flow (rate limit → auth → RBAC → view) hold under adversarial inputs?
6. Backwards compatibility concerns — would changing middleware order break existing clients?
7. Cross-cutting concerns — do error responses from middleware vs views use consistent formats?

Be creative. Think like an attacker probing the full stack, not a developer testing a single function.

Here is the source code:
```

## Files to paste after the prompt

Paste the contents of these files in order:
1. `config/settings.py`
2. `config/urls.py`
3. `middleware/rate_limiter.py`
4. `middleware/auth.py`
5. `middleware/request_logger.py`
6. `api/urls.py`
7. `api/views.py`

---

## Running with Ollama (recommended)

```bash
# Concatenate all source files and pipe to the model
cat config/settings.py config/urls.py middleware/rate_limiter.py \
    middleware/auth.py middleware/request_logger.py \
    api/urls.py api/views.py | \
ollama run deepseek-coder-v2:16b "$(cat prompts/01-generate-scenarios.md | sed -n '/^```$/,/^```$/p' | sed '1d;$d')

$(cat)"
```

Or simply copy the prompt + source code into any LLM chat interface.
