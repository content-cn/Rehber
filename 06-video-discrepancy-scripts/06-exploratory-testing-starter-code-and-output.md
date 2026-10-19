# Exploratory Testing — Starter Code and Output

## Goal
Record the missing content proof for exploratory testing: starter code snapshot plus generated outputs.

## What to show
1. Open `03-ai-exploratory-testing/sample-app/starter-code/README.md`
2. Show the real app files under `sample-app/` that form the starter state:
   - `middleware/rate_limiter.py`
   - `middleware/auth.py`
   - `config/settings.py`
   - `api/urls.py`
3. Explain that the starter state is the Django app before any scenarios are generated
4. Open `03-ai-exploratory-testing/sample-app/final-output/scenarios.txt`
5. Open `03-ai-exploratory-testing/sample-app/final-output/test_results.txt`
6. Open `03-ai-exploratory-testing/sample-app/final-output/output.txt`
7. Explain the progression: codebase → generated scenarios → captured curl results → structured bug report

## Voice-over
- "For exploratory testing, the starter code is the Django app itself."
- "The generated artifacts are kept separately so the flow is easy to understand in the repo."
- "This lets a reviewer see both the input codebase and the final evidence produced by the testing workflow."
