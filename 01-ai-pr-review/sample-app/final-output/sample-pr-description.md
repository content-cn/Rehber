## AI First-Pass Review (Local — Ollama)

Ran `./ai-review.sh main` before pushing. Findings addressed:

1. **Bug (Fixed):** Was retrying all non-2xx errors including 400/401/403/404.
   Now only retries 429/500/502/503/504.
2. **Bug (Fixed):** Was ignoring Retry-After header on 429 responses.
   Now reads and respects the header.
3. **Warning (Fixed):** Exponential backoff had no upper bound.
   Added `max_delay=30` cap.
4. **Warning (Fixed):** Only caught `HTTPError`, missing `ConnectionError`/`Timeout`.
   Now catches all transient network failures.

AI review shows clean. Ready for human review focused on design/architecture.
