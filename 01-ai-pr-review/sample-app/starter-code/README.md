# Starter Code

This folder contains the exact starter state for the AI PR Review demo before the AI findings are applied.

## What is included
- `utils/http_client.py` — the intentionally flawed retry handler used on the feature branch
- `utils/__init__.py`
- `ai-review.sh` — the local PR review script

## How to use it in the demo
1. Initialize a git repo.
2. Create a `main` branch with a placeholder `utils/http_client.py` as shown in the Part B script.
3. Create the feature branch.
4. Copy `starter-code/utils/http_client.py` into `utils/http_client.py` on the feature branch.
5. Run `./ai-review.sh main`.

## Expected outcome
The AI review should flag retrying non-retryable HTTP errors, ignoring `Retry-After`, uncapped backoff, and missing network exception handling.
