# AI-Generated Unit Tests & Coverage Boost — FREE Version (No API Keys)

**What's different from the paid version:**
- Uses **Ollama** (free, local LLM) instead of OpenAI/Anthropic API keys
- Source code **never leaves your machine** — data privacy is a non-issue
- Uses **Qodo Cover CLI + Ollama backend** for the same agentic generate-run-fix loop
- Bug-surfacing prompt runs through Ollama locally (or free ChatGPT/Claude.ai web interface as fallback)
- Total cost: **$0**

---

## PART A — Hook Script (~1 minute)

> **[HOOK — open with the pain point]**
>
> You've got a module with 12% test coverage. Every change is a leap of faith. You know you need tests — but writing them manually for every branch, every edge case? That's days of work nobody signs up for.
>
> **[HIGH-LEVEL WORKFLOW]**
>
> In this video, I'll show you how to go from 12% to 80%+ coverage in minutes — completely free, no API keys, and your code never leaves your machine.
>
> Here's the stack:
> 1. **Ollama** — runs an open-source coding LLM locally on your laptop. No cloud, no API key, no cost.
> 2. **Qodo Cover** — an open-source CLI tool that plugs into Ollama and runs an autonomous generate-run-fix loop: it writes a test, runs it, reads the failure, rewrites, retries — all without you touching the keyboard.
> 3. After the tests are generated, we run a **bug-surfacing pass** — the AI doesn't just validate the current code, it actively looks for bugs like off-by-one errors, wrong operators, missing edge cases. It turns from a test writer into a code auditor.
> 4. Everything goes through a **PR for human review**. Nothing merges without your sign-off.
>
> **[BENEFITS]**
>
> This works across Python, JavaScript, and Java. Your code stays local — no data privacy concerns. And the bug-surfacing step can catch issues that have been hiding in your code for months. All of this, completely free.
>
> **[CTA]**
>
> I'll walk through the entire setup — install commands, exact prompts, and a live demo where you watch the coverage climb in real time. Keep watching Part B.

---

## SCREEN RECORDING — Suggested Video Splits

| Video | Steps Covered | Description | Est. Duration |
|-------|--------------|-------------|---------------|
| **Video 1** | Pre-requisites | Install Ollama, pull model, install Qodo Cover, create sample project | 8-12 min |
| **Video 2** | Step 1 | Coverage baseline — run pytest, show 23% starting point | 3-5 min |
| **Video 3** | Steps 2-3 | Run Qodo Cover with Ollama — watch the agentic loop live | 12-18 min |
| **Video 4** | Step 4 | Verify coverage improvement — before/after delta | 3-5 min |
| **Video 5** | Step 5 | Bug-surfacing pass — local AI catches planted bugs | 8-10 min |
| **Video 6** | Steps 6-7 | Review generated tests + submit PR | 5-8 min |

**Recording reminders:**
- Light theme on all tools (IDE/terminal/GitHub/browser)
- Normal speed, no fast-forwarding
- Voice-over throughout — call out:
  - **"This is the wow factor"** when the agentic loop auto-corrects a failing test (Video 3)
  - **"This is the game-changer"** when the bug-surfacing prompt finds the planted bugs (Video 5)
  - **"And all of this is running locally — no API keys, no cloud, your code stays on your machine"** (mention at least twice)
- Do not crop/trim before uploading

---

## PART B — Detailed Implementation Script

---

### PRE-REQUISITES SETUP

#### B0.1 — Install Ollama

Ollama lets you run open-source LLMs locally. No account, no API key, no cloud.

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

Start the Ollama server (it runs in the background):
```bash
ollama serve
```

**Say in recording:** *"Ollama runs LLMs entirely on your machine. No API key, no account creation, no cloud. Your code never leaves your laptop — which completely eliminates the data privacy concern we'd have with cloud-based LLMs."*

#### B0.2 — Pull a Code-Optimized Model

We need a model that's good at writing code. Pull **qwen2.5-coder:7b** — it's optimized for code tasks and runs on most modern laptops (needs ~8GB RAM):

```bash
ollama pull qwen2.5-coder:7b
```

Verify the model is available:
```bash
ollama list
```

You should see `qwen2.5-coder:7b` in the output.

**Alternative models (if you have more RAM):**

| Model | RAM Needed | Quality |
|-------|-----------|---------|
| `qwen2.5-coder:7b` | ~8 GB | Good — recommended for most laptops |
| `deepseek-coder-v2:16b` | ~16 GB | Very good — if you have the RAM |
| `qwen2.5-coder:32b` | ~32 GB | Excellent — closest to cloud-model quality |

**Say in recording:** *"I'm using qwen2.5-coder, a 7-billion parameter model that's specifically trained for code. It fits on most laptops. If you have more RAM, you can pull a larger model for better results — I'll put the alternatives on screen."*

#### B0.3 — Install Qodo Cover

```bash
pip install qodo-cover
```

Verify:
```bash
cover-agent --help
```

#### B0.4 — Install Test Dependencies

```bash
pip install pytest pytest-cov
```

#### B0.5 — Create the Sample Project

Create the project structure:
```bash
mkdir -p ai-test-demo/app ai-test-demo/tests
cd ai-test-demo
touch app/__init__.py tests/__init__.py
```

**Create the source file** — `app/calculator.py`:

```python
"""A simple calculator module with deliberately low test coverage and a subtle bug."""


def add(a, b):
    """Return the sum of two numbers."""
    return a + b


def subtract(a, b):
    """Return the difference of two numbers."""
    return a - b


def multiply(a, b):
    """Return the product of two numbers."""
    return a * b


def divide(a, b):
    """Return the division of a by b. Raises ValueError for division by zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def calculate_discount(price, discount_percent):
    """Return the final price after applying a discount percentage (0-100).
    Should reject negative prices and discounts outside 0-100 range."""
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount must be between 0 and 100")
    # BUG: Does not validate negative prices (docstring says it should)
    discount_amount = price * (discount_percent / 100)
    return price - discount_amount


def find_max_in_list(numbers):
    """Return the maximum value in a non-empty list of numbers."""
    if not numbers:
        raise ValueError("List cannot be empty")
    max_val = numbers[0]
    for i in range(1, len(numbers)):
        # BUG: Uses < instead of > — this actually finds the MINIMUM
        if numbers[i] < max_val:
            max_val = numbers[i]
    return max_val


def is_palindrome(text):
    """Check if text is a palindrome (case-insensitive, ignoring spaces)."""
    cleaned = text.lower().replace(" ", "")
    return cleaned == cleaned[::-1]


def fizzbuzz(n):
    """Return 'FizzBuzz' for multiples of both 3 and 5, 'Fizz' for multiples of 3,
    'Buzz' for multiples of 5, or the number as a string."""
    if n % 15 == 0:
        return "FizzBuzz"
    elif n % 3 == 0:
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    return str(n)
```

**Create a minimal test file** — `tests/test_calculator.py`:

```python
"""Minimal existing tests - only covers add()."""
from app.calculator import add


def test_add_positive():
    assert add(2, 3) == 5


def test_add_negative():
    assert add(-1, -1) == -2
```

**Say in recording:** *"We have a calculator module with 7 functions but only 2 tests covering add(). There are also two planted bugs — find_max_in_list uses the wrong comparison operator, and calculate_discount doesn't validate negative prices. Let's see if our local AI catches them."*

#### B0.6 — Initialize Git

```bash
git init
git add .
git commit -m "Initial commit: calculator module with minimal tests"
```

#### B0.7 — Quick Sanity Check — Verify Ollama + Code Model Works

Before running the full pipeline, verify the model responds to code prompts:

```bash
ollama run qwen2.5-coder:7b "Write a single pytest test for a function called subtract(a, b) that returns a - b. Output only the Python code."
```

You should get a working test function back. If this works, you're ready.

---

### STEP 1 — Establish a Coverage Baseline

**Say in recording:** *"Let's see where we start."*

```bash
pytest tests/ --cov=app --cov-report=xml:coverage.xml --cov-report=term
```

Expected output:
```
tests/test_calculator.py ..                                    [100%]

---------- coverage: ----------
Name                  Stmts   Miss  Cover
-----------------------------------------
app/calculator.py        35     27    23%
-----------------------------------------
TOTAL                    35     27    23%
```

**Say in recording:** *"23% coverage. Only add() is tested. Let's get this to 80% using a local AI model — no cloud, no API key."*

---

### STEP 2 — Run Qodo Cover with Ollama Backend

**🎬 This is where the magic starts.**

```bash
cover-agent \
  --source-file-path "app/calculator.py" \
  --test-file-path "tests/test_calculator.py" \
  --code-coverage-report-path "coverage.xml" \
  --test-command "pytest tests/test_calculator.py --cov=app --cov-report=xml:coverage.xml" \
  --coverage-type "cobertura" \
  --desired-coverage 80 \
  --max-iterations 5 \
  --model "ollama/qwen2.5-coder:7b"
```

**Explain each flag while it starts running:**

| Flag | Purpose |
|------|---------|
| `--source-file-path` | The file to increase coverage for |
| `--test-file-path` | Where new tests are written (appends to existing) |
| `--code-coverage-report-path` | The coverage XML that Qodo Cover reads |
| `--test-command` | Exact command to run tests and regenerate coverage |
| `--coverage-type` | Coverage report format |
| `--desired-coverage` | Stop when this threshold is reached |
| `--max-iterations` | **BREAKPOINT** — caps retries to prevent context pollution |
| `--model` | **`ollama/qwen2.5-coder:7b`** — tells Qodo Cover to use the local Ollama model instead of a cloud API |

**Say in recording:** *"Notice the --model flag. We're pointing it at ollama/qwen2.5-coder:7b. This tells Qodo Cover to call our local Ollama server instead of OpenAI or Anthropic. No API key needed. And the --max-iterations flag is our guardrail — if a test can't be fixed in 5 attempts, it stops to avoid burning through context and wasting compute."*

---

### STEP 3 — Watch the Agentic Generate-Run-Fix Loop

**🎬 WOW FACTOR MOMENT #1 — Call this out.**

As Qodo Cover runs, the terminal shows the loop in action:

```
[Iteration 1] Analyzing source: app/calculator.py
[Iteration 1] Generating tests for uncovered functions: subtract, multiply, divide...
[Iteration 1] Running generated tests...
[Iteration 1] test_subtract_basic: PASSED ✓
[Iteration 1] test_multiply_by_zero: PASSED ✓
[Iteration 1] test_divide_by_zero_raises: FAILED ✗
  > Expected ValueError, got different assertion
[Iteration 1] Analyzing failure...
[Iteration 2] Rewriting test_divide_by_zero_raises...
[Iteration 2] test_divide_by_zero_raises: PASSED ✓
[Iteration 2] Coverage: 52%
[Iteration 3] Generating tests for: calculate_discount, find_max_in_list, is_palindrome, fizzbuzz...
...
```

**Say in recording:** *"This is the wow factor. Watch — the first attempt at testing divide_by_zero got the assertion wrong. A normal 'write me a test' prompt would've just given you a broken test and stopped. But the agentic loop reads the failure, understands what went wrong, rewrites the test, and re-runs it. Self-correcting. And all of this is running on our local model — no cloud, no API calls, no cost per token."*

**Key things to point out:**
- Tests that pass first try (simple functions)
- Tests that fail and get auto-fixed (wrong assertions, missing imports)
- If `--max-iterations` is hit: *"The guardrail kicked in. Instead of an infinite retry loop polluting the context window, it stopped cleanly. We can take this specific test up in a fresh session."*

**Note on speed:** Local models are slower than cloud APIs. A 7B model on a laptop may take 30-60 seconds per test generation attempt. This is normal — mention it:

**Say in recording:** *"You'll notice it's a bit slower than a cloud API — that's the trade-off for running locally. But we're paying zero dollars and our code stays on our machine. For a one-time coverage boost on a module, the extra minutes are worth it."*

---

### STEP 4 — Verify Coverage Improvement

```bash
pytest tests/test_calculator.py --cov=app --cov-report=term-missing
```

Expected output:
```
---------- coverage: ----------
Name                  Stmts   Miss  Cover   Missing
----------------------------------------------------
app/calculator.py        35      7    80%    33, 45-47
----------------------------------------------------
TOTAL                    35      7    80%
```

**Say in recording:** *"23% to 80%. The 'Missing' column shows lines 33 and 45-47 — inside calculate_discount and find_max_in_list. Those are actually where our planted bugs live. Let's see if the AI catches them in the next step."*

---

### STEP 5 — Bug-Surfacing Pass (AI as Code Auditor)

**🎬 WOW FACTOR MOMENT #2 — THE GAME-CHANGER.**

**Say in recording:** *"Here's the game-changer. Most people think AI test generation just validates what the code already does. But what if the code is wrong? The AI happily writes a test that confirms the bug. So we add a dedicated step — we ask the AI to put on its code reviewer hat and actively look for bugs. And we're doing this entirely locally."*

#### B5.1 — Run the bug-surfacing prompt through Ollama

Create a file called `bug_surfacing_prompt.txt`:

```text
You are a senior code reviewer. I will provide you with a source code file and its corresponding unit tests.

Your task is NOT to validate the tests. Instead, analyze the SOURCE CODE for potential bugs.

Look for:
1. Off-by-one errors in loops or boundary conditions.
2. Incorrect operator usage (e.g., < vs <=, == vs !=).
3. Missing null/empty/edge-case checks (e.g., negative inputs, empty strings).
4. Logic that contradicts function naming or docstrings.
5. Edge cases that would produce incorrect results.

For each potential bug found, explain:
- What the issue is
- Which line(s) are affected
- What the expected behavior likely should be (based on function name/docstring)
- A suggested fix

If no bugs are found, state that explicitly.
```

Now run it with the source code piped in:

```bash
echo "$(cat bug_surfacing_prompt.txt)

--- SOURCE CODE (app/calculator.py) ---
$(cat app/calculator.py)

--- UNIT TESTS (tests/test_calculator.py) ---
$(cat tests/test_calculator.py)" | ollama run qwen2.5-coder:7b
```

#### B5.2 — Alternative: Use free ChatGPT or Claude.ai web (no API key needed)

If you prefer a more powerful model for this one-off analysis, open [chat.openai.com](https://chat.openai.com) or [claude.ai](https://claude.ai) (both free, no API key needed) and paste the same prompt with your source code and tests. This is a manual step but uses a stronger model for the bug-surfacing analysis.

**Say in recording:** *"For the bug-surfacing step, you have two options. You can run it locally through Ollama — keeping everything on your machine. Or if you want a more powerful analysis for this one step, paste it into the free tier of ChatGPT or Claude.ai — no API key needed, just the web interface. Since this is a one-time analysis and we're using a non-sensitive demo project, either approach works."*

#### B5.3 — Expected AI findings

The AI should identify both planted bugs:

**Bug 1 — `find_max_in_list` uses wrong comparison:**
```
Function: find_max_in_list
Line: if numbers[i] < max_val  (line ~47)
Issue: The comparison operator is < but the function is named "find_max"
and the docstring says "Return the maximum value." Using < actually finds
the MINIMUM value, not the maximum.
Fix: Change < to >
```

**Bug 2 — `calculate_discount` missing negative price check:**
```
Function: calculate_discount
Lines: 31-34
Issue: The docstring says "Should reject negative prices" but the code only
validates discount_percent. A negative price (e.g., -100) is accepted and
produces an incorrect result.
Fix: Add: if price < 0: raise ValueError("Price cannot be negative")
```

**Say in recording:** *"The AI found both bugs — running entirely on our local machine. It caught the wrong operator in find_max_in_list and the missing validation in calculate_discount. These are exactly the kind of subtle bugs that pass code review because the code 'looks right' at first glance. Without this step, the AI would have written tests that confirm the buggy behavior. This is what makes this technique genuinely powerful — and we did it with zero API keys, zero cost."*

#### B5.4 — Fix the bugs and update tests

Apply the fixes:

```python
# Fix 1: find_max_in_list - change < to >
    for i in range(1, len(numbers)):
        if numbers[i] > max_val:    # was: numbers[i] < max_val
            max_val = numbers[i]

# Fix 2: calculate_discount - add negative price validation
def calculate_discount(price, discount_percent):
    if price < 0:
        raise ValueError("Price cannot be negative")
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount must be between 0 and 100")
    discount_amount = price * (discount_percent / 100)
    return price - discount_amount
```

Re-run tests:
```bash
pytest tests/test_calculator.py -v
```

**Say in recording:** *"After fixing the bugs, some AI-generated tests that validated the wrong behavior will now fail — that's expected and correct. We update those assertions to match the fixed logic. Now our test suite is both comprehensive AND correct."*

---

### STEP 6 — Review Generated Tests

Open `tests/test_calculator.py` in your IDE.

**Point out in recording:**
- Tests match existing style (function naming, assertions)
- Edge cases covered (empty lists, zero division, boundary conditions)
- Each test has a descriptive name
- No unnecessary complexity

**Say in recording:** *"This is the human-in-the-loop step. Everything AI generated is a draft. Check that assertions are meaningful, not just 'assert True.' Make sure tests actually test what the function name says. The developer has the final say — always."*

---

### STEP 7 — Submit as a PR

```bash
git checkout -b ai/add-unit-tests
git add tests/ app/
git commit -m "Add AI-generated unit tests (coverage: 23% -> 80%) + fix 2 bugs found by AI"
git push origin ai/add-unit-tests
```

Open a PR on GitHub:
- **Title:** `AI-Generated Unit Tests — Coverage 23% → 80% + 2 Bugs Fixed`
- **Description:** Coverage before/after, functions now covered, bugs surfaced and fixed.

**Say in recording:** *"The PR is the final gate. Your team reviews the tests like any other code. Nothing merges without human approval. And let's recap what we just did — we went from 23% to 80% coverage, found and fixed two bugs, and did it all for free with no API keys and no code leaving our machine. The same technique works with JavaScript and Jest, or Java and JUnit — it's completely language agnostic."*

---

## TROUBLESHOOTING

### Ollama model is slow
Local models on CPU are slower than cloud APIs. Tips:
- Close other heavy applications to free RAM
- Use a smaller model (`qwen2.5-coder:3b`) if 7B is too slow — quality drops but speed improves
- If you have an NVIDIA GPU, Ollama uses it automatically for much faster inference

### Qodo Cover can't connect to Ollama
Make sure the Ollama server is running:
```bash
ollama serve
```
It should be listening on `http://localhost:11434`. Verify:
```bash
curl http://localhost:11434/api/tags
```

### Tests keep failing after max-iterations
This is the breakpoint working as designed. The test couldn't be fixed in N attempts. Options:
1. Try a larger model (`deepseek-coder-v2:16b` if you have 16GB+ RAM)
2. Start a fresh session — context pollution from previous failures may be the cause
3. Write that specific test manually — not every test is worth AI-generating

### Model produces low-quality tests
Smaller local models (7B) produce slightly lower quality than GPT-4o or Claude. Mitigate by:
- Using the largest model your hardware supports
- Increasing `--max-iterations` to give more retry attempts
- Reviewing and manually improving the weakest generated tests

---

## COST & PRIVACY SUMMARY

| Aspect | This Approach | Cloud API Approach |
|--------|--------------|-------------------|
| **Cost** | $0 | $0.01-0.10+ per run (API tokens) |
| **API Key Required** | No | Yes (OpenAI or Anthropic) |
| **Code Leaves Machine** | Never | Yes — sent to cloud LLM |
| **Data Privacy Risk** | None | Depends on provider terms |
| **Speed** | Slower (30-60s per generation on CPU) | Fast (5-10s per generation) |
| **Test Quality** | Good (7B) to Excellent (32B) | Excellent (GPT-4o/Claude) |
| **Setup Complexity** | Install Ollama + pull model | Get API key + set env var |

**Say in recording (closing):** *"If your org has strict data privacy policies, this is the approach. Code never leaves your machine. If speed matters more and you have API access, the cloud version is faster. Either way, the technique is the same — and that's the real takeaway."*
