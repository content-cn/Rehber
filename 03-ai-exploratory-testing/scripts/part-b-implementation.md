# AI Exploratory Testing — E2E Flow Testing with Local LLMs — Part B: Detailed Implementation

> **Purpose:** Step-by-step walkthrough. Every command, file, prompt, and expected output.
> **Video cues:** 🎬 = wow factor, 🎥 = recording start/stop, 🗣️ = voice-over cue.
> **LLM:** All prompts are LLM-agnostic. Demo uses Ollama with deepseek-coder-v2:16b but any LLM works.

---

## PRE-REQUISITES SETUP

🎥 *Start recording — Video 1*

### B0.1 — Install Ollama (recommended for local/private execution)

**macOS:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Start the server:
```bash
ollama serve
```

🗣️ *"I'm using Ollama to run the LLM locally — no API key, no cloud, code stays on my machine. But the prompts we'll use are LLM-agnostic. You can copy them into ChatGPT, Claude, Gemini, or any coding model. No vendor lock-in."*

---

### B0.2 — Pull a 16B+ Parameter Model

E2E flow analysis across middleware requires strong reasoning — 16B minimum recommended.

```bash
ollama pull deepseek-coder-v2:16b
```

Verify:
```bash
ollama list
```

**Alternative models (show on screen):**

| Model | RAM | Quality | Interface |
|-------|-----|---------|-----------|
| `deepseek-coder-v2:16b` | ~16 GB | Recommended — strong multi-file reasoning | Ollama |
| `qwen2.5-coder:32b` | ~32 GB | Best local quality | Ollama |
| GPT-4o / Claude 3.5 Sonnet | Cloud | Excellent — but code leaves your machine | Web/API |
| Any coding-capable model | Varies | Will work — prompt is portable | Any |

🗣️ *"I'm using deepseek-coder-v2 16B — it's strong at multi-file code analysis. For E2E flow testing across middleware, you need at least a 16B parameter model. Smaller models may miss cross-file interactions."*

---

### B0.3 — Install Django and Set Up the Sample App

```bash
cd sample-app
pip install django djangorestframework
python manage.py migrate
```

Start the server:
```bash
python manage.py runserver 8000
```

Quick sanity check:
```bash
curl -s http://localhost:8000/api/health | python -m json.tool
```

Expected:
```json
{
    "status": "ok",
    "service": "demo-api",
    "version": "1.2.0"
}
```

🗣️ *"A Django backend with 9 endpoints across 4 categories: public, authenticated, admin with RBAC, and internal behind API keys. Three middleware layers: request logger, rate limiter, and auth. Happy-path tests would pass. Let's trace the full flow and see what breaks."*

🎥 *End recording — Video 1*

---

## STEP 1 — Walk Through the Codebase

🎥 *Start recording — Video 2*

Open each file in the IDE briefly. **Do NOT point out bugs.** Let the AI find them.

### B1.1 — Middleware stack (show `config/settings.py`)

🗣️ *"Three middleware layers, in this order: request logger, rate limiter, then auth. Every request passes through all three before reaching a view. The order matters."*

Show the `MIDDLEWARE` list:
```python
MIDDLEWARE = [
    "middleware.request_logger.RequestLoggerMiddleware",
    "middleware.rate_limiter.RateLimiterMiddleware",
    "middleware.auth.APIAuthMiddleware",
]
```

### B1.2 — Rate limiter (show `middleware/rate_limiter.py`)

🗣️ *"Standard rate limiter — tracks requests per IP, enforces a limit per time window. Looks reasonable."*

### B1.3 — Auth middleware (show `middleware/auth.py`)

🗣️ *"Auth middleware handles three tiers: public endpoints skip auth, internal endpoints need an API key, everything else needs a Bearer token with RBAC. There's a user store with three users — alice (viewer), bob (editor), carol (admin) — each with different permissions."*

### B1.4 — Views (show `api/views.py`)

🗣️ *"The views themselves are straightforward — product listing, order management, admin panel, internal metrics. The interesting part isn't the views — it's the middleware chain in front of them. Let's NOT look for bugs ourselves. Let's feed this entire codebase to the AI and see what it traces."*

### B1.5 — URLs (show `api/urls.py`)

Show the 9 endpoints briefly.

🎥 *End recording — Video 2*

---

## STEP 2 — Feed the Codebase to the LLM for Scenario Generation

🎥 *Start recording — Video 3*

### 🎬 WOW FACTOR MOMENT #1 — The AI traces the full middleware chain.

### B2.1 — Open Prompt 1

Open `prompts/01-generate-scenarios.md` and show the prompt on screen.

🗣️ *"This prompt asks the AI to trace the COMPLETE request lifecycle — rate limiter → auth → RBAC → view → response. Not just test endpoints, but test the full vertical. Like fuzzing the E2E flow. This prompt works in any LLM — I'm using Ollama locally but you could paste this into ChatGPT, Claude, or Gemini."*

### B2.2 — Feed the codebase

**Option A — Ollama CLI:**
```bash
cat config/settings.py config/urls.py \
    middleware/rate_limiter.py middleware/auth.py middleware/request_logger.py \
    api/urls.py api/views.py | \
ollama run deepseek-coder-v2:16b "$(cat prompts/01-generate-scenarios.md | sed -n '/^```$/,/^```$/{ /^```$/d; p; }' | head -30)

$(cat)"
```

**Option B — Any LLM chat interface:**
1. Copy the prompt from `prompts/01-generate-scenarios.md`
2. Paste it into ChatGPT / Claude / Gemini / any LLM
3. Then paste the contents of all 7 source files

### B2.3 — Wait for output (30-90 seconds locally)

🗣️ *(while waiting)* *"The AI is reading our middleware stack, our auth logic, our URL configuration — the full codebase. It's tracing request paths to figure out which middleware runs for which endpoints, and looking for gaps in the E2E flow."*

### B2.4 — Walk through the generated scenarios

Expected output (will vary by model but should capture these patterns):

```
---
SCENARIO: Rate limiter bypass via POST method
CATEGORY: Rate Limiter Flaw
FLOW TRACE: Request → RequestLogger → RateLimiter (SKIPPED — method is POST) → Auth → View
TESTING: Whether non-GET methods bypass rate limiting entirely
CURL:
for i in $(seq 1 200); do
  curl -s -o /dev/null -w "%{http_code}\n" -X POST http://localhost:8000/api/orders/create \
    -H "Authorization: Bearer token-user-bob" \
    -H "Content-Type: application/json" \
    -d '{"product_id": 1, "quantity": 1}'
done
EXPECTED: After 100 requests, subsequent POSTs should be rate-limited (429)
PREDICTED ISSUE: The rate limiter only checks GET requests (if request.method != "GET": return).
All POST/PUT/DELETE requests bypass rate limiting entirely — an attacker can flood write endpoints.
---

---
SCENARIO: Internal endpoint accepts any API key value
CATEGORY: Auth Bypass
FLOW TRACE: Request → RequestLogger → RateLimiter → Auth._check_api_key() → View
TESTING: Whether internal endpoints validate the actual API key or just check for presence
CURL:
curl -s http://localhost:8000/api/internal/config \
  -H "X-API-Key: literally-any-string"
EXPECTED: 401 Unauthorized — the key "literally-any-string" is not a valid API key
PREDICTED ISSUE: _check_api_key() only checks `if not api_key` — it verifies the header
EXISTS but never compares against settings.INTERNAL_API_KEY. Any non-empty string passes.
---

---
SCENARIO: RBAC bypass with partial permissions
CATEGORY: RBAC Flaw
FLOW TRACE: Request → RequestLogger → RateLimiter → Auth._check_bearer_token() → _check_permissions() → View
TESTING: Whether a user with only ONE of the required permissions can access a restricted endpoint
CURL:
curl -s http://localhost:8000/api/admin/users \
  -H "Authorization: Bearer token-user-alice"
EXPECTED: 403 Forbidden — alice has "read:products" and "read:orders" but NOT "read:users" or "admin:export"
PREDICTED ISSUE: _check_permissions() uses set intersection (OR logic) instead of subset (AND logic).
Required: ["read:users", "admin:export"]. Alice has "read:orders" — but if there's ANY overlap
between alice's permissions and the required set, she passes. Check if alice's permissions
intersect with {"read:users", "admin:export"} — they don't, so this specific test may pass.
BUT: bob with ["read:products", "write:products", "read:orders"] trying /api/orders/create
(requires ["write:orders", "read:products"]) — bob has "read:products" which intersects,
so bob would pass even though he lacks "write:orders".
---

---
SCENARIO: Path matching bypass — auth skip via URL manipulation
CATEGORY: Auth Bypass
FLOW TRACE: Request → RequestLogger → RateLimiter → Auth (PUBLIC_PATHS startswith check) → View
TESTING: Whether adding a suffix to a public path bypasses auth for non-public endpoints
CURL:
curl -s http://localhost:8000/api/products-admin/secret
EXPECTED: 404 or 401 — this path doesn't exist and shouldn't bypass auth
PREDICTED ISSUE: PUBLIC_PATHS uses `path.startswith("/api/products")` — the path
"/api/products-admin/secret" starts with "/api/products" so it matches as public
and SKIPS auth entirely. Even though it doesn't map to a valid URL, the auth bypass
pattern itself is dangerous.
---

---
SCENARIO: Rate limiter returns 200 on limit exceeded
CATEGORY: Rate Limiter Flaw
FLOW TRACE: Request → RequestLogger → RateLimiter (limit exceeded) → STOP (returns response)
TESTING: What HTTP status code the rate limiter returns when blocking a request
CURL:
# First, exhaust the rate limit
for i in $(seq 1 101); do
  curl -s -o /dev/null http://localhost:8000/api/products
done
# Then check the response
curl -s -w "\nHTTP_STATUS: %{http_code}\n" http://localhost:8000/api/products
EXPECTED: 429 Too Many Requests
PREDICTED ISSUE: The rate limiter returns JsonResponse(..., status=200).
Clients checking HTTP status codes will think rate-limited requests SUCCEEDED.
This is a wrong rejection policy — automated clients and load balancers
depend on 429 to implement backoff.
---

---
SCENARIO: IP spoofing to bypass rate limiter
CATEGORY: Security
FLOW TRACE: Request → RequestLogger → RateLimiter._get_client_ip() → rate check
TESTING: Whether an attacker can bypass rate limiting by rotating X-Forwarded-For headers
CURL:
for i in $(seq 1 200); do
  curl -s -o /dev/null http://localhost:8000/api/products \
    -H "X-Forwarded-For: 10.0.0.$((i % 255))"
done
echo "All 200 requests should have been rate-limited but weren't"
EXPECTED: Rate limiting should use the real client IP, not a client-provided header
PREDICTED ISSUE: _get_client_ip() trusts X-Forwarded-For blindly without validation.
An attacker can rotate fake IPs in the header to get a fresh rate limit window per request.
---

---
SCENARIO: Internal config endpoint exposes secrets
CATEGORY: Security
FLOW TRACE: Request → Logger → RateLimiter → Auth._check_api_key() (accepts any key) → internal_config view
TESTING: Whether sensitive config data is exposed through the internal endpoint
CURL:
curl -s http://localhost:8000/api/internal/config \
  -H "X-API-Key: anything" | python -m json.tool
EXPECTED: This endpoint should be strictly protected — it returns config including secret key preview
PREDICTED ISSUE: Combined with the API key bypass (any key accepted), this endpoint
leaks internal configuration: debug mode, database engine, rate limit settings,
and a preview of the SECRET_KEY. Authentication + information disclosure compound.
---
```

🗣️ *"Look at this. The AI didn't just test endpoints — it TRACED the full request flow for each scenario. For the rate limiter bypass, it shows: Request → Logger → RateLimiter SKIPPED because method is POST → Auth → View. It traced the middleware chain and found the gap. For the RBAC bypass, it walked through _check_permissions() and identified that set intersection is OR logic, not AND."*

*"These are exactly the issues a senior engineer who understands the full stack would find during a thorough code review — but most teams don't have time for that kind of deep-dive on every release."*

**Key point:** *"And these prompts are LLM-agnostic. I'm running this on Ollama locally, but the same prompt works in ChatGPT, Claude, or Gemini. No vendor lock-in."*

### B2.5 — Save the scenarios

```bash
# Save to a file for reference
# (if using Ollama CLI, redirect output)
# If using a web LLM, copy-paste the output to scenarios.txt
```

🎥 *End recording — Video 3*

---

## STEP 3 — Run the Scenarios Against the Live App (TDD Approach)

🎥 *Start recording — Video 4*

🗣️ *"This is the TDD part. We don't assume the AI's predictions are correct — we test and capture actual behavior. Run each curl against the live app and record what actually comes back."*

Make sure Django is running on port 8000.

### B3.1 — Test: Rate limiter returns 200 instead of 429

```bash
# Exhaust the rate limit (100 GET requests)
for i in $(seq 1 101); do
  curl -s -o /dev/null http://localhost:8000/api/products
done

# Check what the 102nd request returns
curl -s -w "\nHTTP_STATUS: %{http_code}\n" http://localhost:8000/api/products
```

**Actual result:** `HTTP_STATUS: 200` with `{"error": "Rate limit exceeded. Try again later."}`

🗣️ *"200 OK. The rate limiter blocked us but returned a 200 status code. Any automated client, load balancer, or monitoring tool checking status codes will think this request SUCCEEDED. That's a wrong rejection policy — it should be 429."*

Save to test_results.txt:
```bash
echo "=== Test: Rate limiter wrong status code ===" > test_results.txt
echo "CURL: GET /api/products (after 101 requests)" >> test_results.txt
echo "RESPONSE STATUS: 200" >> test_results.txt
echo 'RESPONSE BODY: {"error": "Rate limit exceeded. Try again later."}' >> test_results.txt
echo "" >> test_results.txt
```

---

### B3.2 — Test: POST bypasses rate limiter

```bash
# Create 150 orders rapidly (should be rate-limited but won't be)
for i in $(seq 1 150); do
  curl -s -o /dev/null -w "%{http_code} " -X POST http://localhost:8000/api/orders/create \
    -H "Authorization: Bearer token-user-bob" \
    -H "Content-Type: application/json" \
    -d '{"product_id": 1, "quantity": 1}'
done
echo ""
```

**Actual result:** All 150 return `201`. No rate limiting applied.

🗣️ *"150 POST requests, zero throttling. The rate limiter only checks GET. All write operations — POST, PUT, DELETE — bypass it entirely. An attacker could flood your write endpoints."*

---

### B3.3 — Test: Internal endpoint accepts any API key

```bash
curl -s http://localhost:8000/api/internal/config \
  -H "X-API-Key: literally-any-string" | python -m json.tool
```

**Actual result:** `200 OK` — returns internal config including secret key preview.

🗣️ *"Any string works as an API key. The middleware checks if the header exists but never validates the value. And now we can see internal config — debug mode, database engine, and a preview of the SECRET_KEY. Authentication bypass + information disclosure."*

---

### B3.4 — Test: RBAC OR vs AND

```bash
# Bob has ["read:products", "write:products", "read:orders"]
# /api/orders/create requires ["write:orders", "read:products"]
# Bob lacks "write:orders" but has "read:products" — with OR logic, he passes
curl -s -X POST http://localhost:8000/api/orders/create \
  -H "Authorization: Bearer token-user-bob" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 1}'
```

**Actual result:** `201 Created` — Bob can create orders even though he lacks `write:orders`.

🗣️ *"Bob doesn't have the write:orders permission. But because the RBAC check uses OR logic — set intersection instead of subset — having ANY one matching permission is enough. Bob has read:products, which overlaps, so he passes. This should require ALL permissions."*

---

### B3.5 — Test: Path matching bypass

```bash
curl -s http://localhost:8000/api/products-admin/secret
```

**Actual result:** `404 Not Found` — but crucially, no 401. Auth was *skipped*.

🗣️ *"404 because the URL doesn't map to a view. But the important thing is: no 401. Auth was completely bypassed because /api/products-admin starts with /api/products, which is in the public paths list. If someone added an endpoint at that path, it would be accessible without auth."*

---

### B3.6 — Test: IP spoofing bypass

```bash
# Send 200 requests with rotating fake IPs
for i in $(seq 1 200); do
  curl -s -o /dev/null -w "%{http_code} " http://localhost:8000/api/products \
    -H "X-Forwarded-For: 10.0.0.$((i % 255))"
done
echo ""
```

**Actual result:** All return `200`. Rate limiting bypassed via IP rotation.

🗣️ *"200 requests, all successful. The rate limiter trusts X-Forwarded-For blindly. An attacker can rotate fake IPs and get a fresh rate limit window every time."*

---

### B3.7 — Test: No token expiry validation

```bash
# Tokens in the user store have no expiry timestamp
# A token that should have been revoked or expired still works indefinitely
curl -s http://localhost:8000/api/orders \
  -H "Authorization: Bearer token-user-alice"
```

**Actual result:** `200 OK` — returns alice's orders. The token has no expiry mechanism — it works forever.

🗣️ *"This token has no expiry. In a real system, if alice's account is deactivated or her token is revoked, this token would still work indefinitely. There's no timestamp, no TTL, no revocation check. Tokens should have a bounded lifetime."*

---

### B3.8 — Save all results

Append all test results to `test_results.txt` with the format shown above.

🎥 *End recording — Video 4*

---

## STEP 4 — Feed Results Back to AI for Bug Report

🎥 *Start recording — Video 5*

### 🎬 WOW FACTOR MOMENT #2 — Structured bug report with flow traces.

### B4.1 — Open Prompt 2

Open `prompts/02-analyze-results.md` and show the prompt.

🗣️ *"Same approach — copy the prompt into your LLM, paste the test results. The AI will trace through the middleware chain for each result and produce a structured bug report."*

### B4.2 — Feed results to the LLM

**Option A — Ollama CLI:**
```bash
ollama run deepseek-coder-v2:16b "$(cat prompts/02-analyze-results.md | sed -n '/^```$/,/^```$/{ /^```$/d; p; }' | head -30)

$(cat test_results.txt)"
```

**Option B:** Paste prompt + test_results.txt into any LLM chat.

### B4.3 — Walk through the bug report

Expected output:

```
BUG ID: B001
SEVERITY: Critical
TITLE: Rate limiter returns HTTP 200 on rejection — wrong rejection policy
COMPONENT: Rate Limiter Middleware
FLOW TRACE: Request → Logger → RateLimiter → BLOCKED but returns 200 instead of 429
IMPACT: Automated clients, load balancers, and monitoring tools rely on 429 to implement
backoff. Returning 200 means clients process the error body as a successful response.
Upstream services will not know to slow down.
FIX: middleware/rate_limiter.py — change status=200 to status=429. Add Retry-After header.
REGRESSION NOTE: Any client parsing the JSON error body (instead of checking status codes)
may need to be updated to handle 429. Verify upstream consumers.

BUG ID: B002
SEVERITY: Critical
TITLE: Rate limiter only applies to GET — all write methods bypass
COMPONENT: Rate Limiter Middleware
FLOW TRACE: POST/PUT/DELETE → Logger → RateLimiter (SKIPPED) → Auth → View
IMPACT: An attacker can send unlimited POST/PUT/DELETE requests — creating thousands of
orders, updating data, or triggering expensive operations without any throttle.
FIX: middleware/rate_limiter.py — remove the `if request.method != "GET"` check.
Apply rate limiting to all methods, or use method-specific limits.
REGRESSION NOTE: Existing batch import scripts may need rate limit exceptions.

BUG ID: B003
SEVERITY: Critical
TITLE: Internal endpoints accept any API key — value not validated
COMPONENT: Auth Middleware
FLOW TRACE: Request → Logger → RateLimiter → Auth._check_api_key() → only checks existence → View
IMPACT: Any request with a non-empty X-API-Key header can access internal endpoints
including /api/internal/config which leaks secret key, debug mode, and database config.
FIX: middleware/auth.py — add: if api_key != settings.INTERNAL_API_KEY: return 401
REGRESSION NOTE: Ensure all internal service consumers use the correct key from settings.

BUG ID: B004
SEVERITY: High
TITLE: RBAC uses OR logic instead of AND — partial permission bypass
COMPONENT: Auth Middleware
FLOW TRACE: Request → Logger → RateLimiter → Auth → _check_permissions() → set intersection (OR)
IMPACT: Users with ANY one matching permission can access endpoints requiring ALL listed
permissions. Bob with "read:products" can access /api/orders/create which requires
["write:orders", "read:products"].
FIX: middleware/auth.py — change `return bool(user_perms & required)` to
`return required.issubset(user_perms)`
REGRESSION NOTE: Users who previously had access may lose it. Audit current user permissions.

...

SUMMARY:
- Total: 7 bugs
- Critical: 3 (rate limiter status, rate limiter method bypass, API key not validated)
- High: 2 (RBAC OR vs AND, IP spoofing)
- Medium: 2 (path matching bypass, no token expiry)

MIDDLEWARE HEALTH:
- Request Logger: ✅ Clean
- Rate Limiter: ❌ 3 issues (wrong status, method bypass, IP spoofing)
- Auth: ❌ 4 issues (API key not validated, RBAC OR logic, path matching, no expiry)

TOP 3 PRIORITY FIXES:
1. B003 — Validate API key value (leaks secrets RIGHT NOW)
2. B001+B002 — Fix rate limiter status + method coverage (DDoS vector)
3. B004 — Fix RBAC to AND logic (privilege escalation)

BACKWARDS COMPATIBILITY NOTES:
- B001: Clients parsing error body instead of status codes will need updates
- B002: Batch scripts may need rate limit exceptions
- B004: Some users may lose access — audit permissions before deploying
```

🗣️ *"Seven bugs across two middleware components. Three critical — including an API key that's never validated, which right now is leaking internal config to anyone who sends the header. The AI gave us a full middleware health report, a priority list, and backwards compatibility notes for each fix."*

**Key point:** *"This is what E2E flow testing catches that unit tests miss. Unit tests would verify that _check_api_key() returns 401 when the header is empty. They wouldn't test that ANY non-empty string passes — because the unit test would use the correct key. You need to trace the full flow, like fuzzing, to find these gaps."*

*"And this also works as regression testing between releases. Save these scenarios, re-run them before every deployment, and verify the middleware chain still holds."*

🎥 *End recording — Video 5*

---

## STEP 5 — Fix Critical Issues and Verify

🎥 *Start recording — Video 6*

### B5.1 — Fix the rate limiter

In `middleware/rate_limiter.py`:

**Fix 1 — Correct status code:**
```python
# Before:
return JsonResponse({"error": "Rate limit exceeded..."}, status=200)
# After:
return JsonResponse(
    {"error": "Rate limit exceeded. Try again later."},
    status=429,
    headers={"Retry-After": str(self.window)},
)
```

**Fix 2 — Apply to all methods:**
```python
# Remove this block entirely:
if request.method != "GET":
    return self.get_response(request)
```

**Fix 3 — Don't trust X-Forwarded-For blindly:**
```python
def _get_client_ip(self, request):
    # Only trust X-Forwarded-For behind a known reverse proxy
    # In production, validate against TRUSTED_PROXIES list
    return request.META.get("REMOTE_ADDR")
```

---

### B5.2 — Fix auth middleware

In `middleware/auth.py`:

**Fix 4 — Validate API key value:**
```python
def _check_api_key(self, request):
    api_key = request.META.get("HTTP_X_API_KEY", "")
    if not api_key or api_key != settings.INTERNAL_API_KEY:
        return JsonResponse({"error": "Invalid API key"}, status=401)
    return self.get_response(request)
```

**Fix 5 — RBAC AND logic:**
```python
def _check_permissions(self, user, required_permissions):
    user_perms = set(user.get("permissions", []))
    required = set(required_permissions)
    return required.issubset(user_perms)  # AND — all required must be present
```

**Fix 6 — Exact path matching:**
```python
# Before:
if any(path.startswith(p) for p in PUBLIC_PATHS):
# After:
if path in PUBLIC_PATHS:
```

---

### B5.3 — Re-run the failing scenarios

```bash
# Rate limiter: should now return 429
curl -s -w "\nHTTP_STATUS: %{http_code}\n" http://localhost:8000/api/products
# (after exhausting limit)

# Internal endpoint: invalid key should fail
curl -s -w "\nHTTP_STATUS: %{http_code}\n" http://localhost:8000/api/internal/config \
  -H "X-API-Key: literally-any-string"
# Expected: 401

# RBAC: Bob should be denied
curl -s -w "\nHTTP_STATUS: %{http_code}\n" -X POST http://localhost:8000/api/orders/create \
  -H "Authorization: Bearer token-user-bob" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 1}'
# Expected: 403
```

🗣️ *"429 on rate limit. 401 on invalid API key. 403 on insufficient permissions. All fixed. The middleware chain is now production-ready."*

🎥 *End recording — Video 6*

---

## CLOSING RECAP

🗣️ *"Let's recap what we did:*

*1. We took a Django backend with three middleware layers — rate limiter, auth, RBAC. It works fine on happy paths. Unit tests would pass.*

*2. We fed the full codebase to an LLM — settings, middleware, views, URL config — and asked it to trace the complete request lifecycle end-to-end. Like fuzzing the middleware stack.*

*3. The AI generated 15 E2E test scenarios with flow traces showing exactly which middleware runs, what it checks, and where the flow breaks down.*

*4. We ran the curls against the live app — TDD approach, test and capture real behavior — and fed the results back to the AI.*

*5. The AI produced a structured bug report: 7 issues, 3 critical, across the rate limiter and auth middleware. Wrong rejection policy, method bypass, API key not validated, RBAC using OR instead of AND, path matching bypass, IP spoofing. All invisible to unit tests.*

*6. We fixed everything and verified the middleware chain holds.*

*This reduces manual regression testing between releases — save the scenarios, re-run before every deployment. It proves your business logic is intact end-to-end and doesn't deviate from the design specification. The AI even flags which fixes could break existing clients — backwards compatibility notes built into the bug report.*

*The prompts work with ANY LLM — Ollama, ChatGPT, Claude, Gemini. No vendor lock-in. And they're tech stack portable — same prompts work on Django, Flask, Express, Spring Boot. Any backend with middleware.*

*Fewer bugs that unit tests can't catch. Faster releases. Reduced testing time. Copy the prompt templates, point them at your codebase, and see what the AI finds in YOUR middleware stack."*

---

## CONSTRAINTS & NOTES

1. **16B+ model recommended:** Multi-file E2E analysis needs strong reasoning. 7B models may miss cross-file interactions.
2. **LLM agnostic:** Prompts are plain text — work with any LLM. No API-specific code.
3. **TDD approach:** Always run curls and capture real behavior. Don't assume the AI's predictions are correct.
4. **Regression testing:** Save scenarios and re-run between releases to verify backwards compatibility.
5. **Not a security audit replacement:** Catches common middleware flaws but not a substitute for OWASP/pentest.
6. **Tech stack portable:** Prompts work on Django, Flask, Express, Spring Boot — any backend with middleware.
7. **Data privacy (Ollama):** When running locally, code never leaves your machine.
