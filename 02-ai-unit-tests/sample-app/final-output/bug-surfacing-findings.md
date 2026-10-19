# Expected Bug-Surfacing Findings

## Bug 1 — `find_max_in_list`
- **Issue:** Uses `<` instead of `>` inside the loop
- **Impact:** Returns the minimum value instead of the maximum
- **Fix:** Change the comparison to `if numbers[i] > max_val:`

## Bug 2 — `calculate_discount`
- **Issue:** Accepts negative price values despite docstring contract
- **Impact:** Produces invalid discounted totals for negative inputs
- **Fix:** Add `if price < 0: raise ValueError("Price cannot be negative")`

## Expected narration point
After fixing `calculator.py`, some previously AI-generated tests may fail if they encoded the buggy behavior. Update those assertions before opening the PR.
