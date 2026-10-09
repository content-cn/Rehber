"""Rate Limiter Middleware — controls request throughput per IP.

Planted bugs (DO NOT fix until AI finds them):
1. Returns 200 with JSON error body instead of 429 status code (wrong rejection policy)
2. Only rate-limits GET requests — POST/PUT/DELETE bypass the limiter entirely
3. Uses client-provided X-Forwarded-For header for IP without validation (IP spoofing)
"""

import time
from django.http import JsonResponse
from django.conf import settings


# In-memory store: {ip: [timestamps]}
_request_log = {}


class RateLimiterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.max_requests = getattr(settings, "RATE_LIMIT_REQUESTS", 100)
        self.window = getattr(settings, "RATE_LIMIT_WINDOW_SECONDS", 60)

    def __call__(self, request):

        client_ip = self._get_client_ip(request)
        now = time.time()

        if client_ip not in _request_log:
            _request_log[client_ip] = []

        # Clean old entries
        _request_log[client_ip] = [
            t for t in _request_log[client_ip] if now - t < self.window
        ]

        if len(_request_log[client_ip]) >= self.max_requests:
            # BUG 1: Returns 200 with error body instead of 429
            # Clients checking HTTP status codes will think this succeeded
            return JsonResponse(
                {"error": "Rate limit exceeded. Try again later."},
                status=429,
                headers={"Retry-After": str(self.window)},
            )

        _request_log[client_ip].append(now)
        return self.get_response(request)

    def _get_client_ip(self, request):
        return request.META.get("REMOTE_ADDR")
