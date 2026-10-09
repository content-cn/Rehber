"""Request Logger Middleware — logs every request for debugging.

No intentional bugs — this middleware is clean.
It sits first in the middleware chain so it captures the full lifecycle.
"""

import time
import logging

logger = logging.getLogger("api.requests")


class RequestLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()
        response = self.get_response(request)
        duration = time.time() - start

        logger.info(
            "%s %s → %s (%.3fs)",
            request.method,
            request.path,
            response.status_code,
            duration,
        )
        return response
