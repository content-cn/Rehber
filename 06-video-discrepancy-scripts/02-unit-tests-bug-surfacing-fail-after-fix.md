# Unit Tests — Show Existing Tests Failing After Fixing `calculator.py`

## Goal
Record the missing moment where AI-generated tests encode buggy behavior, then fail after the source bug is fixed.

## What to show
1. Start from the generated test suite in `02-ai-unit-tests/sample-app/final-output/tests/test_calculator.py`
2. Explain that AI-generated tests may reflect current implementation, not intended behavior
3. Open the buggy starter source in `starter-code/app/calculator.py`
4. Open the fixed source in `final-output/app/calculator.py`
5. Say that after applying the fix, any assertions expecting the old buggy behavior should fail
6. Demonstrate by temporarily describing the pre-fix expectation:
   - `find_max_in_list([3, 9, 2, 5])` would have incorrectly returned `2`
   - negative price might have been accepted in the buggy version
7. Run:
   ```bash
   pytest tests/test_calculator.py -v
   ```
8. Call out the failing assertions that need to be updated to match intended behavior

## Voice-over
- "This is the subtle risk with AI-generated tests: they can validate the bug if the source code is wrong."
- "The failing test here is actually good news — it proves the bug fix changed behavior."
- "Now we update the tests so they reflect the intended contract, not the old bug."
