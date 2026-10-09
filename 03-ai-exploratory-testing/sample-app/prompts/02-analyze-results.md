# Prompt 2: Analyze Test Results and Produce Bug Report

> **How to use:** After running the curl commands from Prompt 1 against your live API, copy the prompt below into your LLM and paste all the curl commands + their actual responses.

---

## Prompt

```
You are a senior QA engineer analyzing end-to-end exploratory test results from a Django REST API.

I ran a series of curl commands against the live application and captured the actual HTTP responses. Analyze each result by tracing through the full middleware chain (rate limiter → auth → RBAC → view) and determine if the behavior is correct or indicates a bug.

For each BUG found, use this exact format:

---
BUG ID: [B001, B002, etc.]
SEVERITY: [Critical | High | Medium | Low]
TITLE: [Short title]
COMPONENT: [Rate Limiter Middleware | Auth Middleware | RBAC Logic | View | URL Config]
FLOW TRACE: [The full request path and where it broke down]
DESCRIPTION: [What went wrong]
REPRODUCTION: [The exact curl command]
ACTUAL RESPONSE: [What the API returned — status code + body]
EXPECTED RESPONSE: [What a correct implementation should return]
IMPACT: [What could go wrong in production — data exposure, auth bypass, etc.]
FIX: [Suggested code change with file and line reference]
REGRESSION NOTE: [If fixing this could break existing clients or flows, note it here]
---

At the end, provide:
1. SUMMARY — total bugs by severity
2. MIDDLEWARE HEALTH — which middleware components have issues and which are clean
3. TOP 3 PRIORITY FIXES — ordered by production impact
4. BACKWARDS COMPATIBILITY NOTES — which fixes could affect existing consumers

Here are the test results:
```

## What to paste after the prompt

For each test, paste in this format:
```
=== Test: [scenario name] ===
CURL: curl -s [full command]
RESPONSE STATUS: [HTTP status code]
RESPONSE BODY:
[actual response body]
```

---

## Running with Ollama (recommended)

```bash
ollama run deepseek-coder-v2:16b "$(cat prompts/02-analyze-results.md | sed -n '/^```$/,/^```$/p' | head -1 | sed '1d;$d')

$(cat test_results.txt)"
```

Or paste the prompt + test results into any LLM chat interface.
