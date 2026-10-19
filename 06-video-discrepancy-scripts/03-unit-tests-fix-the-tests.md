# Unit Tests — Fix the Tests After the Source Bug Fix

## Goal
Record the follow-up video where the test suite is corrected after the source logic is fixed.

## What to show
1. Open `02-ai-unit-tests/sample-app/final-output/tests/test_calculator.py`
2. Update any assertions that were validating buggy behavior
3. Ensure these expectations are visible on screen:
   - `find_max_in_list([3, 9, 2, 5]) == 9`
   - `calculate_discount(-100, 10)` raises `ValueError`
4. Re-run:
   ```bash
   pytest tests/test_calculator.py -v
   ```
5. If useful, also show:
   ```bash
   pytest tests/test_calculator.py --cov=app --cov-report=term-missing
   ```
6. End on a passing test suite

## Voice-over
- "First we fixed the code, then we fixed the tests to match the intended behavior."
- "That human review step is mandatory — AI gives you a draft, not a guarantee."
- "Now the suite is both broad in coverage and correct in meaning."
