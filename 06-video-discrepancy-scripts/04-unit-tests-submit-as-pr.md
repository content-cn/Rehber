# Unit Tests — Submit as a PR

## Goal
Record the missing PR submission segment for the unit-test workflow.

## What to show
1. Create a branch:
   ```bash
   git checkout -b ai/add-unit-tests
   ```
2. Stage and commit:
   ```bash
   git add tests/ app/ coverage.xml
   git commit -m "Add AI-generated unit tests and fix surfaced bugs"
   ```
3. Open `02-ai-unit-tests/sample-app/final-output/sample-pr-description.md`
4. Copy the PR title and summary into GitHub
5. Show the PR diff highlighting:
   - larger test suite
   - bug fixes in `calculator.py`
   - coverage artifact included
6. End on the open PR screen

## Voice-over
- "Nothing merges directly. The PR is the human approval gate."
- "I'm including both the coverage gain and the surfaced bug fixes in the PR description."
- "The reviewer can now focus on whether the tests reflect intended business logic."
