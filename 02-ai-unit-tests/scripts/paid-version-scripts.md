# AI-Generated Unit Tests & Coverage Boost — Scripts

---

## PART A — Hook Script (~1 minute)

> **[HOOK — open with the pain point]**
>
> You inherit a module with 12% test coverage. Every time you touch it, you hold your breath and pray nothing breaks. You know you should write tests — but manually covering every branch, every edge case, every error path? That's days of work nobody wants to do.
>
> **[HIGH-LEVEL WORKFLOW — what we're building]**
>
> In this video, I'll show you how to use AI to take that module from 12% to 80%+ coverage — in minutes, not days — using Qodo Cover, an open-source CLI tool, backed by Claude or GPT-4o.
>
> Here's what happens:
> 1. You point the tool at a file with low coverage.
> 2. AI reads your code, understands the logic, and generates real unit tests — not generic stubs — matching your existing test style.
> 3. It runs them automatically. If a test fails, it reads the error, understands WHY it failed, rewrites the test, and retries — an autonomous generate-run-fix loop with built-in guardrails so it doesn't burn your tokens.
> 4. Then — and this is the game-changer — we run a dedicated bug-surfacing pass. AI doesn't just validate the current code. It actively looks for bugs: off-by-one errors, wrong operators, missing edge cases. It turns from a test writer into a code auditor.
> 5. Everything goes through a PR for human review. Nothing merges without your sign-off.
>
> **[BENEFITS]**
>
> This approach works across Python, JavaScript, and Java — same tool, same technique, truly language agnostic. Your test-debt backlog that nobody wants to tackle? AI handles the heavy lifting. And the bug-surfacing step can catch issues that have been hiding in your code for months.
>
> **[CTA]**
>
> I'll walk you through the entire setup step by step — actual CLI commands, the exact prompts, and a live demo where you can see the coverage number climb in real time. Keep watching Part B.

---

## SCREEN RECORDING — Suggested Video Splits

Split recordings at these logical breakpoints:

| Video | Steps Covered | Description | Est. Duration |
|-------|--------------|-------------|---------------|
| **Video 1** | Pre-requisites | Environment setup: Python, pip install, API keys, sample project with a planted bug | 5-8 min |
| **Video 2** | Step 1 | Establish coverage baseline — run pytest, show the 12% starting point | 3-5 min |
| **Video 3** | Steps 2-3 | Run Qodo Cover CLI — watch the agentic loop in action (generate, fail, fix, retry) | 10-15 min |
| **Video 4** | Step 4 | Verify coverage improvement — show the before/after delta | 3-5 min |
| **Video 5** | Step 5 | Bug-surfacing pass — run the dedicated prompt, show AI finding a real bug | 8-10 min |
| **Video 6** | Steps 6-7 | Review tests + submit PR with coverage diff and bug report | 5-8 min |

**Recording reminders:**
- Light theme on all tools (IDE, terminal, GitHub, browser)
- Record at normal speed, no fast-forwarding
- Voice-over throughout — call out:
  - **"This is the wow factor"** when the generate-run-fix loop auto-corrects a failing test (Video 3)
  - **"This is the game-changer"** when the bug-surfacing prompt catches the planted bug (Video 5)
  - **"This is the portable pattern"** — mention this works identically with Jest/JUnit
- Do not crop/trim before uploading
- Update this Part B script if you discover better approaches during recording

---

## PART B — Detailed Implementation Script

---

### PRE-REQUISITES SETUP

#### B0.1 — Python Environment

1. Ensure **Python 3.8+** is installed:
   ```bash
   python3 --version
   ```
2. Create a project directory (or use an existing repo):
   ```bash
   mkdir ai-test-demo && cd ai-test-demo
   python3 -m venv venv
   source venv/bin/activate
   ```

#### B0.2 — Install Qodo Cover

1. Install the CLI tool:
   ```bash
   pip install qodo-cover
   ```
2. Verify installation:
   ```bash
   cover-agent --help
   ```

**Say in recording:** *"Qodo Cover — formerly called Cover-Agent — is an open-source tool from Qodo that implements the agentic test generation loop we're about to see. It's language agnostic — works with Python, JavaScript, Java, and more."*

#### B0.3 — Install Test Dependencies

```bash
pip install pytest pytest-cov
```

#### B0.4 — Set Up LLM API Key

Set your API key as an environment variable. Use either OpenAI or Anthropic:

```bash
# Option A: OpenAI
export OPENAI_API_KEY="sk-your-openai-key-here"

# Option B: Anthropic (Claude)
export ANTHROPIC_API_KEY="sk-ant-your-anthropic-key-here"
```

**Data privacy note (mention in video):** *"Quick disclaimer — when you run this tool, your source code is sent to the LLM provider for analysis. Most enterprise organizations have data partitioning agreements that ensure your proprietary code is never used for model training. But if you're working on a sensitive codebase, check your org's policies first. This isn't unique to this tool — it applies to Cursor, Copilot, Claude Code, or any AI coding assistant."*

#### B0.5 — Create the Sample Project

We need a Python module with low test coverage and at least one subtle bug for the demo.

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
    # BUG: Does not validate negative prices
    discount_amount = price * (discount_percent / 100)
    return price - discount_amount


def find_max_in_list(numbers):
    """Return the maximum value in a non-empty list of numbers."""
    if not numbers:
        raise ValueError("List cannot be empty")
    max_val = numbers[0]
    for i in range(1, len(numbers)):
        # BUG: Uses < instead of > — finds minimum, not maximum
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
"""Minimal existing tests — only covers add()."""
from app.calculator import add


def test_add_positive():
    assert add(2, 3) == 5


def test_add_negative():
    assert add(-1, -1) == -2
```

**Create `__init__.py` files:**
```bash
touch app/__init__.py tests/__init__.py
```

**Say in recording:** *"I've set up a simple calculator module with 7 functions but only 2 tests — covering just the add() function. There are also two planted bugs: find_max_in_list uses the wrong comparison operator, and calculate_discount doesn't validate negative prices. Let's see if the AI catches them."*

#### B0.6 — Initialize Git

```bash
git init
git add .
git commit -m "Initial commit: calculator module with minimal tests"
```

---

### STEP 1 — Establish a Coverage Baseline

**Say in recording:** *"Before we run anything, let's see where we stand. This is our 'before' number."*

#### B1.1 — Run existing tests with coverage

```bash
pytest tests/ --cov=app --cov-report=xml:coverage.xml --cov-report=term
```

#### B1.2 — Read the output

Expected output will look something like:
```
tests/test_calculator.py ..                                    [100%]

---------- coverage: ----------
Name                  Stmts   Miss  Cover
-----------------------------------------
app/calculator.py        35     27    23%
-----------------------------------------
TOTAL                    35     27    23%
```

**Say in recording:** *"23% coverage. Only add() is tested. The other 6 functions — subtract, multiply, divide, calculate_discount, find_max_in_list, is_palindrome, fizzbuzz — have zero tests. Let's fix that."*

---

### STEP 2 — Invoke Qodo Cover with Target Threshold and Retry Breakpoint

**🎬 This is where the agentic AI kicks in.**

#### B2.1 — Run the CLI command

```bash
cover-agent \
  --source-file-path "app/calculator.py" \
  --test-file-path "tests/test_calculator.py" \
  --code-coverage-report-path "coverage.xml" \
  --test-command "pytest tests/test_calculator.py --cov=app --cov-report=xml:coverage.xml" \
  --coverage-type "cobertura" \
  --desired-coverage 80 \
  --max-iterations 5
```

#### B2.2 — Explain each flag (while it starts running)

| Flag | Purpose |
|------|---------|
| `--source-file-path` | The file we want to increase coverage for |
| `--test-file-path` | Where to write the new tests (appends to existing file) |
| `--code-coverage-report-path` | The coverage XML report for Qodo Cover to read |
| `--test-command` | The exact command Qodo Cover will run to execute tests and regenerate coverage |
| `--coverage-type` | Format of the coverage report (cobertura, lcov, etc.) |
| `--desired-coverage` | Target threshold — stop when this is reached |
| `--max-iterations` | **THE BREAKPOINT** — caps the retry loop to prevent token burndown and context pollution |

**Say in recording:** *"The --max-iterations flag is critical. Without it, the tool could keep retrying failed tests indefinitely, burning through your API tokens and polluting the context window with accumulated failures. Setting it to 5 means: if a test can't be fixed in 5 attempts, stop and move on. You can always take unconverged tests up in a fresh session."*

---

### STEP 3 — Observe the Agentic Generate-Run-Fix Loop

**🎬 WOW FACTOR MOMENT #1 — Call this out.**

#### B3.1 — Watch the terminal output

As Qodo Cover runs, you'll see output like:
```
[Iteration 1] Generating tests for: subtract, multiply, divide...
[Iteration 1] Running generated tests...
[Iteration 1] test_subtract_positive: PASSED ✓
[Iteration 1] test_multiply_by_zero: PASSED ✓
[Iteration 1] test_divide_by_zero_raises: FAILED ✗
  > AssertionError: Expected ValueError but got ZeroDivisionError
[Iteration 1] Analyzing failure for test_divide_by_zero_raises...
[Iteration 2] Rewriting test_divide_by_zero_raises with corrected assertion...
[Iteration 2] Running rewritten test...
[Iteration 2] test_divide_by_zero_raises: PASSED ✓
[Iteration 2] Current coverage: 58%
[Iteration 3] Generating tests for uncovered branches: calculate_discount, find_max_in_list...
...
```

**Say in recording:** *"This is the wow factor right here. Watch what happens — the first attempt at testing divide got the exception type wrong. A normal 'write me a test' prompt would've just given you a broken test. But the agentic loop reads the failure, understands the actual exception type is ValueError not ZeroDivisionError, rewrites the assertion, and re-runs. It's self-correcting. That's the difference between a single prompt and an autonomous agent."*

#### B3.2 — Point out key behaviors

- **Tests that pass immediately** — simple functions like `subtract`, `multiply`
- **Tests that fail and get auto-fixed** — wrong assertion types, missing imports, incorrect mock setups
- **Tests that hit max-iterations** — if any test can't converge in 5 tries, the tool stops cleanly and reports it

**Say in recording (if max-iterations is hit):** *"Notice that the tool stopped after 5 attempts on this test. This is the guardrail in action — instead of burning through tokens with an infinite retry loop, it reports the failure and lets you handle it in a fresh session where the context isn't polluted by previous failed attempts."*

#### B3.3 — Context pollution explained (mention briefly)

**Say in recording:** *"A quick note on why the breakpoint matters. Context pollution happens when the LLM's context window fills up with stale, conflicting information from repeated failed attempts. Each failed retry adds noise — old error messages, outdated assertions — that can confuse the model and make subsequent attempts worse, not better. Capping iterations and starting a fresh session is the production-grade approach."*

---

### STEP 4 — Verify Coverage Improvement

#### B4.1 — Run the coverage command

```bash
pytest tests/test_calculator.py --cov=app --cov-report=term-missing
```

#### B4.2 — Show the before/after

Expected output:
```
---------- coverage: ----------
Name                  Stmts   Miss  Cover   Missing
----------------------------------------------------
app/calculator.py        35      7    80%    33, 45-47
----------------------------------------------------
TOTAL                    35      7    80%
```

**Say in recording:** *"We went from 23% to 80% coverage. The 'Missing' column shows exactly which lines still need tests — lines 33 and 45-47, which are inside calculate_discount and find_max_in_list. We'll look at those more closely in the bug-surfacing step."*

---

### STEP 5 — Bug-Surfacing Pass (AI as Code Auditor)

**🎬 WOW FACTOR MOMENT #2 — THE GAME-CHANGER. Call this out.**

**Say in recording:** *"Now here's the game-changer. Most people think AI test generation just validates what the code already does. But what if the code is WRONG? The AI will happily write a test that confirms the bug. So we add a separate step — we ask AI to put on its code reviewer hat and actively look for bugs."*

#### B5.1 — Prepare the prompt

Open Claude (claude.ai) or your preferred LLM interface. Use this exact prompt — **this is shareable with viewers:**

```
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

--- SOURCE CODE (app/calculator.py) ---
[PASTE THE FULL SOURCE CODE HERE]

--- UNIT TESTS (tests/test_calculator.py) ---
[PASTE THE FULL TEST FILE HERE INCLUDING AI-GENERATED TESTS]
```

#### B5.2 — Paste source code and tests

1. Copy the full contents of `app/calculator.py` and paste it into the prompt where indicated.
2. Copy the full contents of `tests/test_calculator.py` (now including all AI-generated tests) and paste it.
3. Submit the prompt.

#### B5.3 — Review AI's bug findings

Expected AI output should identify:

**Bug 1 — `find_max_in_list` uses wrong comparison operator:**
```
Line 47: `if numbers[i] < max_val` should be `if numbers[i] > max_val`
The function is named "find_max" and the docstring says "Return the maximum value"
but the comparison `<` actually finds the MINIMUM. This is an incorrect operator bug.
Fix: Change `<` to `>`
```

**Bug 2 — `calculate_discount` missing negative price validation:**
```
Line 31-34: The function validates discount_percent range (0-100) but does NOT
validate that `price` is non-negative. The docstring says "Should reject negative
prices" but the code doesn't implement this check.
Fix: Add `if price < 0: raise ValueError("Price cannot be negative")`
```

**Say in recording:** *"Look at that. The AI found BOTH planted bugs. It caught the wrong comparison operator in find_max_in_list — the function says 'max' but the code finds the minimum. And it caught the missing negative price validation in calculate_discount. These are exactly the kinds of bugs that slip through code review because the code 'looks right' at a glance. And remember — if we had ONLY generated tests without this step, the AI would have written tests that validate the buggy behavior. This bug-surfacing pass is what makes this technique genuinely powerful."*

#### B5.4 — Fix the bugs (optional — show in recording)

```python
# Fix 1: find_max_in_list — change < to >
if numbers[i] > max_val:  # was: if numbers[i] < max_val

# Fix 2: calculate_discount — add price validation
if price < 0:
    raise ValueError("Price cannot be negative")
```

After fixing, re-run tests to confirm the buggy tests now fail (validating the fix):
```bash
pytest tests/test_calculator.py -v
```

**Say in recording:** *"After fixing the bugs, some of the AI-generated tests that were written against the buggy logic will now fail — and that's correct! Those tests were validating wrong behavior. We update them to match the fixed logic, and now our test suite is both comprehensive AND correct."*

---

### STEP 6 — Review Generated Tests and Bug Report

#### B6.1 — Open the test file

Open `tests/test_calculator.py` in your IDE and review the AI-generated tests.

**Point out in recording:**
- Tests match existing style (function naming, assertion patterns)
- Edge cases covered (empty lists, division by zero, boundary conditions)
- Each test has a clear, descriptive name
- No unnecessary mocks or over-complicated setup

#### B6.2 — Human-in-the-loop moment

**Say in recording:** *"This is the human-in-the-loop step. Everything the AI generated is a draft until you review it. Check that assertions are meaningful — not just 'assert True.' Make sure the tests actually test what the function name says. And verify any bug-surfacing findings before acting on them. AI is a powerful assistant, but the developer has the final say."*

---

### STEP 7 — Submit as a PR for Human Review

#### B7.1 — Create a branch and commit

```bash
git checkout -b ai/add-unit-tests
git add tests/
git commit -m "Add AI-generated unit tests (coverage: 23% -> 80%)"
```

#### B7.2 — Push and open a PR

```bash
git push origin ai/add-unit-tests
```

Open a PR on GitHub with:
- **Title:** `AI-Generated Unit Tests — Coverage 23% → 80%`
- **Description:** Include the coverage before/after, list of functions now covered, and any bug-surfacing findings.

**Say in recording:** *"The PR is the final gate. Your team reviews the AI-generated tests just like any other code. Nothing merges without a human sign-off. This is how you get the speed of AI with the quality assurance of a real code review process."*

---

## CONSTRAINTS & NOTES TO MENTION IN VIDEO

1. **Bug-blind testing (Constraint #1):** AI writes tests based on current code. If a bug exists, the test validates the wrong behavior. The bug-surfacing step in Step 5 partially mitigates this, but it's not foolproof. For critical code, provide the AI with specification documents or expected-behavior descriptions alongside the source code.

2. **Code quality dependency (Constraint #2):** Large, messy functions with multiple responsibilities are harder for AI to test and consume more tokens. For best results, refactor the most complex functions first. This is also a good engineering practice regardless of AI.

3. **Data privacy (Constraint #3):** Source code is sent to the LLM provider. Most enterprise orgs have data partitioning agreements. But do your due diligence — review your organization's policies before sharing sensitive codebases with any LLM. This applies to all AI coding tools, not just this workflow.

4. **Context pollution & token burndown:** The `--max-iterations` flag is your guardrail. If a test can't be fixed in N attempts, stop and start a fresh session rather than accumulating noise in the context window.

5. **Language agnostic:** Everything shown here with Python/Pytest works identically with JavaScript/Jest and Java/JUnit. Mention this — it's a key differentiator and value add for viewers.
