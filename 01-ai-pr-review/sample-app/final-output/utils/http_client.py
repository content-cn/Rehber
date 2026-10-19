"""HTTP client utilities for making resilient API calls.
THIS IS THE FIXED VERSION — after AI review findings are applied."""

import time
import requests

# Only retry on these status codes — client errors (4xx except 429) should fail immediately
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


def request_with_retry(method, url, max_retries=3, backoff_factor=2, max_delay=30, **kwargs):
    """Make an HTTP request with automatic retry on failure.

    Retries failed requests with exponential backoff, respecting Retry-After
    headers and only retrying on transient/server errors.

    Args:
        method: HTTP method ('GET', 'POST', etc.).
        url: Target URL.
        max_retries: Maximum number of retry attempts.
        backoff_factor: Multiplier for exponential backoff delay.
        max_delay: Maximum delay between retries in seconds (caps backoff).
        **kwargs: Additional arguments passed to requests.request().

    Returns:
        requests.Response object on success.

    Raises:
        requests.HTTPError: If a non-retryable error occurs or all retries are exhausted.
        requests.ConnectionError: If a network error persists after all retries.
        requests.Timeout: If a timeout persists after all retries.
    """
    last_exception = None

    for attempt in range(max_retries + 1):
        try:
            response = requests.request(method, url, **kwargs)

            if response.status_code not in RETRYABLE_STATUS_CODES:
                response.raise_for_status()
                return response

            if attempt >= max_retries:
                response.raise_for_status()

            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After")
                delay = int(retry_after) if retry_after else backoff_factor ** attempt
            else:
                delay = backoff_factor ** attempt

            delay = min(delay, max_delay)
            time.sleep(delay)

        except (requests.ConnectionError, requests.Timeout) as e:
            last_exception = e
            if attempt >= max_retries:
                raise
            delay = min(backoff_factor ** attempt, max_delay)
            time.sleep(delay)

        except requests.HTTPError:
            raise

    raise last_exception
