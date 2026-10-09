# AI-Powered PR Code Review (Ollama — Free, Local) — Part B: Detailed Implementation

> **Purpose:** Step-by-step walkthrough of the entire setup and demo. Every command, every file, every prompt — nothing skipped.
> **Video cues:** Marked with 🎬 for wow-factor moments and 🎥 for recording instructions.

---

## PRE-REQUISITES SETUP

### B0.1 — Install Ollama

🎥 *Start recording — Video 1*

**macOS:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
Download from [ollama.com/download](https://ollama.com/download).

Start the Ollama server (runs in background):
```bash
ollama serve
```

**🗣️ Say in recording:** *"Ollama lets you run LLMs entirely on your machine. No account, no API key, no cloud calls. Your source code stays on your laptop — which is the whole point for code review."*

---

### B0.2 — Pull a Code-Optimized Model

```bash
ollama pull qwen2.5-coder:7b
```

Verify it's available:
```bash
ollama list
```

You should see `qwen2.5-coder:7b` in the output.

**Alternative models (show as on-screen text):**

| Model | RAM Needed | Quality |
|-------|-----------|---------|
| `qwen2.5-coder:7b` | ~8 GB | Good — works on most laptops |
| `deepseek-coder-v2:16b` | ~16 GB | Better — if you have the RAM |
| `qwen2.5-coder:32b` | ~32 GB | Best — closest to cloud-model quality |

**🗣️ Say in recording:** *"I'm using qwen2.5-coder 7B — a model built specifically for code understanding. Fits on most modern laptops. If you have more RAM, larger models give better reviews — I'll put the alternatives on screen."*

---

### B0.3 — Quick Sanity Check

Verify the model responds to code prompts:

```bash
ollama run qwen2.5-coder:7b "What is wrong with this Python code?

import time
def retry(func, retries=3):
    for i in range(retries):
        try:
            return func()
        except Exception:
            time.sleep(2 ** i)
    raise Exception('All retries failed')"
```

The model should comment on the broad `except Exception`, missing logging, or lack of distinction between retryable and non-retryable errors. Any substantive feedback means we're ready.

**🗣️ Say in recording:** *"Good — the model understands code and gives real feedback. We're ready to build the review pipeline."*

🎥 *End recording — Video 1*

---

## STEP 1 — Set Up the Sample Project with Missing Edge Cases

🎥 *Start recording — Video 2*

### B1.1 — Create the project

```bash
mkdir ai-review-demo && cd ai-review-demo
git init
mkdir utils
touch utils/__init__.py
```

Install the dependency we'll need:
```bash
pip install requests
```

---

### B1.2 — Create the base file on main

Create `utils/http_client.py` on the main branch with a placeholder:

```python
"""HTTP client utilities for making resilient API calls."""


def placeholder():
    """Placeholder — retry logic will be added."""
    pass
```

Commit:
```bash
git add .
git commit -m "Initial commit: project structure with placeholder"
```

---

### B1.3 — Create the feature branch with missing edge cases

```bash
git checkout -b feature/add-retry-logic
```

Now replace `utils/http_client.py` with the full implementation. **This code looks clean, runs without errors, and passes happy-path tests — but has 3 missing edge cases that cause production failures:**

```python
"""HTTP client utilities for making resilient API calls."""

import time
import requests


def request_with_retry(method, url, max_retries=3, backoff_factor=2, **kwargs):
    """Make an HTTP request with automatic retry on failure.

    Retries failed requests with exponential backoff.

    Args:
        method: HTTP method ('GET', 'POST', etc.).
        url: Target URL.
        max_retries: Maximum number of retry attempts.
        backoff_factor: Multiplier for exponential backoff delay.
        **kwargs: Additional arguments passed to requests.request().

    Returns:
        requests.Response object on success.

    Raises:
        requests.HTTPError: If all retries are exhausted.
    """
    last_exception = None

    for attempt in range(max_retries + 1):
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.HTTPError as e:
            last_exception = e
            if attempt < max_retries:
                delay = backoff_factor ** attempt
                time.sleep(delay)

    raise last_exception
```

**🗣️ Say in recording:** *"I've written an HTTP retry handler. It looks clean — exponential backoff, configurable retries, proper exception handling. If you asked Cursor or Copilot to write retry logic, you'd get something almost identical to this. And it works — if you test it against a server that returns a 500 and then a 200, it retries and succeeds. All happy-path tests pass."*

*"But this code has 3 missing edge cases that will cause real problems in production. Let me NOT tell you what they are — let's see if the AI reviewer catches them."*

Commit:
```bash
git add .
git commit -m "Add HTTP client with retry logic"
```

🎥 *End recording — Video 2*

---

## STEP 2 — Create the AI Review Script

🎥 *Start recording — Video 3*

### B2.1 — Write the script

Create `ai-review.sh` in the repo root:

```bash
#!/bin/bash
# AI-Powered Code Review — runs locally via Ollama
# Usage: ./ai-review.sh [base_branch] [model]
# Example: ./ai-review.sh main qwen2.5-coder:7b

BASE_BRANCH="${1:-main}"
MODEL="${2:-qwen2.5-coder:7b}"

echo "🔍 AI Code Review: comparing against '$BASE_BRANCH' using model '$MODEL'"
echo "---"

DIFF=$(git diff "$BASE_BRANCH"...HEAD)

if [ -z "$DIFF" ]; then
    echo "✅ No changes found against $BASE_BRANCH."
    exit 0
fi

PROMPT="You are a senior code reviewer performing a thorough first-pass review on a pull request diff.

Analyze the following git diff carefully and report every issue you find.

For EACH issue, use this exact format:
---
SEVERITY: [Bug | Warning | Style | Suggestion]
FILE: [filename]
LINE: [approximate line or function name]
ISSUE: [Clear description of the problem]
WHY: [Why this is a problem — what could go wrong in production]
FIX: [Specific code change to resolve it]
---

What to look for:
1. Missing edge-case handling that would pass happy-path tests but fail in production
2. HTTP protocol violations (ignoring standard headers, retrying non-retryable status codes)
3. Unbounded loops, delays, or resource usage
4. Exception types that are too narrow or too broad
5. Logic that works for the common case but breaks under adversarial or unexpected inputs
6. Missing input validation (negative numbers, zero, None/null, empty collections)
7. Security issues (injection, path traversal, hardcoded secrets)

IMPORTANT: Think about how this code behaves in production under real-world conditions — not just during local testing with simple inputs.

If no issues are found, respond with: '✅ No issues found. Code looks good.'

Here is the git diff to review:"

echo "$DIFF" | ollama run "$MODEL" "$PROMPT

$(cat)"
```

### B2.2 — Make it executable

```bash
chmod +x ai-review.sh
```

---

### B2.3 — Walk through the script (explain in recording)

**🗣️ Say in recording:** *"Let me walk through what this script does. Three moving parts:"*

1. **`git diff $BASE_BRANCH...HEAD`** — extracts exactly what changed between your branch and main. Same diff you'd see in a GitHub PR.
2. **The prompt** — tells the AI to act as a senior code reviewer. It specifies a structured output format — severity, file, line, issue, why, fix — and lists exactly what to look for. Notice: I've tuned this prompt for *production-readiness*, not just syntax. It specifically asks about HTTP protocol violations, unbounded delays, and edge cases that pass testing but fail in production.
3. **`ollama run $MODEL`** — pipes the diff to the local model. No API call, no network request, no cost. Everything stays on your machine.

*"That's the whole script. It works on any repo, any language — Python, JavaScript, Java, Go. The model reads the diff the same way regardless of language."*

🎥 *End recording — Video 3*

---

## STEP 3 — Run the AI Review

🎥 *Start recording — Video 4*

### 🎬 THE DEMO MOMENT — This is the core of the video.

### B3.1 — Confirm you're on the feature branch

```bash
git branch
```

You should see `* feature/add-retry-logic`.

### B3.2 — Execute the review

```bash
./ai-review.sh main
```

**🗣️ Say in recording:** *"One command. Let's see what it finds."*

### B3.3 — Wait for the output

The model will take 15-60 seconds depending on hardware. You'll see the Ollama spinner while it processes.

**🗣️ Say (while waiting):** *"The model is analyzing our diff locally. On a cloud API this would be near-instant, but we're running on our own hardware — no cost, no API key, no code leaving the machine. A few extra seconds is the trade-off."*

---

## STEP 4 — Observe AI Findings

### 🎬 WOW FACTOR MOMENT — Call this out clearly and enthusiastically.

Expected output (will vary slightly by model, but should catch at least 2-3 of these):

```
🔍 AI Code Review: comparing against 'main' using model 'qwen2.5-coder:7b'
---

---
SEVERITY: Bug
FILE: utils/http_client.py
LINE: except requests.HTTPError (in request_with_retry)
ISSUE: The function retries on ALL non-2xx HTTP status codes, including
non-retryable client errors like 400 (Bad Request), 401 (Unauthorized),
403 (Forbidden), and 404 (Not Found). These errors indicate a problem with
the request itself — retrying will produce the identical failure every time.
WHY: In production, a 401 (expired token) will be retried 3 times with
exponential backoff, wasting 7+ seconds before finally raising — when it
should fail immediately so the caller can refresh the token. A 404 will
never succeed no matter how many times you retry.
FIX: Only retry on retryable status codes. Add a set of retryable codes
and check before retrying:
    RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}
    if response.status_code not in RETRYABLE_STATUS_CODES:
        response.raise_for_status()  # fail immediately, don't retry
---

---
SEVERITY: Bug
FILE: utils/http_client.py
LINE: delay = backoff_factor ** attempt
ISSUE: When a server returns 429 (Too Many Requests), it typically includes
a 'Retry-After' header specifying exactly how long the client should wait
before retrying. This code ignores that header entirely and uses its own
exponential backoff instead.
WHY: Ignoring Retry-After can be too aggressive (retrying before the rate
limit window resets, risking IP bans or account suspension) or too slow
(waiting longer than necessary). Respecting Retry-After is both an HTTP
protocol requirement (RFC 6585) and a practical necessity for staying
within API rate limits.
FIX: Check for Retry-After header on 429 responses:
    if response.status_code == 429:
        retry_after = response.headers.get('Retry-After')
        delay = int(retry_after) if retry_after else backoff_factor ** attempt
    else:
        delay = backoff_factor ** attempt
---

---
SEVERITY: Warning
FILE: utils/http_client.py
LINE: delay = backoff_factor ** attempt
ISSUE: Exponential backoff has no upper bound. With backoff_factor=2, delays
grow as: 1s, 2s, 4s, 8s, 16s, 32s, 64s... If max_retries is set to a higher
value, later retries could have multi-minute delays with no cap.
WHY: An unbounded delay means a single failed request could block a thread
or process for minutes. In a web server context, this could exhaust the
thread pool. In a batch job, it causes unpredictable runtimes.
FIX: Add a max_delay parameter and cap the backoff:
    max_delay = 30  # seconds
    delay = min(backoff_factor ** attempt, max_delay)
---

---
SEVERITY: Warning
FILE: utils/http_client.py
LINE: except requests.HTTPError as e
ISSUE: Only HTTPError is caught. The requests library also raises
ConnectionError (network unreachable, DNS failure), Timeout (request timed
out), and ReadTimeout. These are transient network failures that are
typically the MOST important errors to retry — but they are not caught here
and will crash the function immediately.
WHY: A momentary network blip (e.g., DNS resolution hiccup, load balancer
restart) will crash the caller instead of retrying, defeating the purpose
of having retry logic.
FIX: Catch a broader set of transient exceptions:
    except (requests.HTTPError, requests.ConnectionError,
            requests.Timeout) as e:
---
```

**🗣️ Say in recording:**

*"This — right here — is the wow factor. Let's go through what the AI found."*

*"First: it caught that we're retrying ALL errors, including 401 Unauthorized and 404 Not Found. Retrying a 401 is pointless — the token is expired, retrying won't magically fix it. We should only retry server errors and rate limits — 429, 500, 502, 503, 504."*

*"Second: it caught that we're ignoring the Retry-After header on 429 responses. This is an HTTP protocol requirement — when a server tells you 'wait 30 seconds,' you wait 30 seconds. Our code ignores that and does its own exponential backoff, which could be too aggressive and get us IP-banned."*

*"Third: it flagged that our backoff has no upper bound. With a high retry count, later attempts could wait minutes. That's a thread blocked doing nothing."*

*"And fourth: it caught that we only handle HTTPError but not ConnectionError or Timeout — the most common transient network failures."*

*"Now here's the key point — this is EXACTLY the kind of code that Cursor or Copilot would generate if you asked them to write retry logic. It looks correct. It passes basic tests. But it has real production gaps. The AI coding assistant helped you WRITE the code — but it didn't REVIEW it for production-readiness. That's the gap this fills."*

*"And all of this ran locally. Our code never left this machine."*

🎥 *End recording — Video 4*

---

## STEP 5 — Fix the Flagged Edge Cases

🎥 *Start recording — Video 5*

### B5.1 — Apply all fixes

Open `utils/http_client.py` and replace with the production-ready version:

```python
"""HTTP client utilities for making resilient API calls."""

import time
import requests

# Only retry on these status codes — client errors (4xx except 429) should fail immediately
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


def request_with_retry(method, url, max_retries=3, backoff_factor=2, max_delay=30, **kwargs):
    """Make an HTTP request with automatic retry on failure.

    Retries failed requests with exponential backoff, respecting Retry-After
    headers and only retrying on transient/server errors.

    Args:
        method: HTTP method ('GET', 'POST', etc.).
        url: Target URL.
        max_retries: Maximum number of retry attempts.
        backoff_factor: Multiplier for exponential backoff delay.
        max_delay: Maximum delay between retries in seconds (caps backoff).
        **kwargs: Additional arguments passed to requests.request().

    Returns:
        requests.Response object on success.

    Raises:
        requests.HTTPError: If a non-retryable error occurs or all retries are exhausted.
        requests.ConnectionError: If a network error persists after all retries.
        requests.Timeout: If a timeout persists after all retries.
    """
    last_exception = None

    for attempt in range(max_retries + 1):
        try:
            response = requests.request(method, url, **kwargs)

            # Non-retryable status codes — fail immediately, don't waste retries
            if response.status_code not in RETRYABLE_STATUS_CODES:
                response.raise_for_status()
                return response

            # Retryable status code — but we've exhausted retries
            if attempt >= max_retries:
                response.raise_for_status()

            # Respect Retry-After header on 429
            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After")
                delay = int(retry_after) if retry_after else backoff_factor ** attempt
            else:
                delay = backoff_factor ** attempt

            # Cap the delay
            delay = min(delay, max_delay)
            time.sleep(delay)

        except (requests.ConnectionError, requests.Timeout) as e:
            last_exception = e
            if attempt >= max_retries:
                raise
            delay = min(backoff_factor ** attempt, max_delay)
            time.sleep(delay)

        except requests.HTTPError:
            raise  # Non-retryable HTTP errors already raised above

    raise last_exception
```

**🗣️ Say in recording:** *"Four fixes applied: retryable status code filtering, Retry-After header support, max delay cap, and broader exception handling for network errors. Let's verify the AI is happy."*

---

### B5.2 — Re-run the review to verify clean output

```bash
git add .
git commit -m "Fix retry edge cases: retryable codes, Retry-After, max delay, network errors"
./ai-review.sh main
```

Expected output:
```
✅ No issues found. Code looks good.
```

**🗣️ Say in recording:** *"Clean pass. All four edge cases addressed. Now we're ready for human review."*

---

## STEP 6 — Push and Open a PR

### B6.1 — Push the branch

```bash
git push origin feature/add-retry-logic
```

### B6.2 — Open the PR on GitHub

Create a PR with:
- **Title:** `Add HTTP client with retry logic`
- **Description:**

```markdown
## AI First-Pass Review (Local — Ollama)

Ran `./ai-review.sh main` before pushing. Findings addressed:

1. **Bug (Fixed):** Was retrying all non-2xx errors including 400/401/403/404.
   Now only retries 429/500/502/503/504.
2. **Bug (Fixed):** Was ignoring Retry-After header on 429 responses.
   Now reads and respects the header.
3. **Warning (Fixed):** Exponential backoff had no upper bound.
   Added max_delay=30s cap.
4. **Warning (Fixed):** Only caught HTTPError, missing ConnectionError/Timeout.
   Now catches all transient network failures.

AI review shows clean. Ready for human review focused on design/architecture.
```

**🗣️ Say in recording:** *"I'm including the AI findings in the PR description so the human reviewer knows what was already caught and fixed. They can focus on architecture, design, and business logic — the tedious edge-case hunting was done before the PR was even opened."*

---

## CLOSING RECAP

**🗣️ Say in recording:**

*"Let's recap what we built:*

*1. We installed Ollama and pulled a free, open-source coding model — no account, no API key, no cloud.*

*2. We wrote a shell script that extracts a git diff and feeds it to the local model with a structured code review prompt.*

*3. We ran it on a real feature branch with HTTP retry logic — code that looks correct, passes tests, and is exactly what Cursor or Copilot would generate. The AI reviewer caught 4 missing edge cases that would only surface in production: retrying non-retryable errors, ignoring Retry-After headers, unbounded backoff delays, and missing network error handling.*

*4. We fixed everything, verified a clean pass, and opened a PR. The human reviewer gets a pre-screened, production-hardened PR instead of doing the tedious first pass themselves.*

*This works on Python, JavaScript, Java, Go — any language in a git repo. Code never leaves your machine. And the whole setup is completely free.*

*If you found this useful, copy the ai-review.sh script, run it on your latest feature branch, and see what it catches. You might be surprised."*

🎥 *End recording — Video 5*

---

## CONSTRAINTS & NOTES TO MENTION IN VIDEO

1. **Context window:** Local 7B models handle diffs up to ~500-800 lines well. For very large PRs (1000+ lines), split the diff by file: `git diff main...HEAD -- path/to/file.py`.

2. **Quality vs speed trade-off:** Larger models (16B, 32B) give better reviews but need more RAM and are slower. 7B is the sweet spot for most laptops.

3. **First pass, not a replacement:** AI catches missing edge cases, protocol violations, and unhandled error paths. It won't catch architectural issues, business logic errors, or design problems. Human review remains essential for the second pass.

4. **Language agnostic:** The same script and prompt work on Python, JS, Java, Go, Rust — any language in a git repo. Mention this as a key value add.

5. **Data privacy:** Code never leaves your machine. This is the strongest possible data privacy guarantee — stronger than any enterprise SaaS agreement. Call this out for viewers in regulated industries.

6. **AI-assisted coding vs AI code review:** Cursor/Copilot help you WRITE code. This tool REVIEWS code. They solve different problems. The demo proves this — the retry handler is exactly what an AI coding assistant would generate, and the AI reviewer still found 4 issues in it.
