# Unit Tests — Show `coverage.xml`

## Goal
Record the missing proof that Qodo Cover uses the generated `coverage.xml` file.

## What to show
1. Open `02-ai-unit-tests/sample-app/starter-code/coverage.xml`
2. Point out that this is the baseline coverage report generated from the starter tests
3. Run the baseline command:
   ```bash
   pytest tests/ --cov=app --cov-report=xml:coverage.xml --cov-report=term
   ```
4. Refresh/open `coverage.xml`
5. Run the Qodo Cover command from `scripts/free-version-scripts.md`
6. Show the `--code-coverage-report-path "coverage.xml"` flag on screen
7. After generation, open `02-ai-unit-tests/sample-app/final-output/coverage.xml`
8. Call out that this is the artifact the tool reads and updates during the demo

## Voice-over
- "This `coverage.xml` file is the hand-off between pytest-cov and Qodo Cover."
- "Without this file, the agent doesn't know which lines are still uncovered."
- "I'm showing both the baseline and the final coverage artifact because that was missing earlier."
