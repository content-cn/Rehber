## AI-Generated Unit Tests — Coverage 23% → 80%+ + 2 Bugs Fixed

### Summary
- Increased coverage on `app/calculator.py` from ~23% to 80%+
- Added tests for arithmetic operations, error paths, list handling, and string logic
- Ran a separate bug-surfacing review on source + generated tests
- Fixed 2 real bugs surfaced by AI review

### Bugs fixed
1. `find_max_in_list` returned the minimum due to the wrong comparison operator
2. `calculate_discount` accepted negative prices despite the function contract

### Human review focus
Please review the generated assertions, naming consistency, and whether the test cases reflect the intended business logic after the bug fixes.
