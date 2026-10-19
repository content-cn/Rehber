"""HTTP client utilities for making resilient API calls.
THIS IS THE STARTER / BUGGY VERSION — use this on the feature branch before AI review."""

import time
import requests


def request_with_retry(method, url, max_retries=3, backoff_factor=2, **kwargs):
    """Make an HTTP request with automatic retry on failure.

    Retries failed requests with exponential backoff.

    Args:
        method: HTTP method ('GET', 'POST', etc.).
        url: Target URL.
        max_retries: Maximum number of retry attempts.
        backoff_factor: Multiplier for exponential backoff delay.
        **kwargs: Additional arguments passed to requests.request().

    Returns:
        requests.Response object on success.

    Raises:
        requests.HTTPError: If all retries are exhausted.
    """
    last_exception = None

    for attempt in range(max_retries + 1):
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.HTTPError as e:
            last_exception = e
            if attempt < max_retries:
                delay = backoff_factor ** attempt
                time.sleep(delay)

    raise last_exception
