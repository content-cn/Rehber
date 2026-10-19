# Expected AI Review Output

Representative output to show during the demo:

## Finding 1
- **Severity:** Bug
- **Issue:** Retries all non-2xx HTTP errors including 401 and 404
- **Why it matters:** Non-retryable client errors waste time and hide the real failure
- **Fix:** Retry only `429/500/502/503/504`

## Finding 2
- **Severity:** Bug
- **Issue:** Ignores `Retry-After` header on 429 responses
- **Why it matters:** Can violate server backoff guidance and trigger bans
- **Fix:** Respect `Retry-After` when present

## Finding 3
- **Severity:** Warning
- **Issue:** Exponential backoff has no max cap
- **Why it matters:** Threads/processes can sleep for too long at high retry counts
- **Fix:** Add `max_delay`

## Finding 4
- **Severity:** Warning
- **Issue:** Only catches `requests.HTTPError`
- **Why it matters:** Transient `ConnectionError` / `Timeout` failures are not retried
- **Fix:** Catch transient network exceptions too

## Clean rerun
After applying the fixes, the follow-up AI review should return:

```text
✅ No issues found. Code looks good.
```
