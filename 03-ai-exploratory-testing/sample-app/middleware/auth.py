"""API Auth Middleware — handles token auth and API key checks for internal endpoints.

Planted bugs (DO NOT fix until AI finds them):
1. Internal endpoints behind /api/internal/ only check API key presence, not value
2. RBAC check uses OR instead of AND — user with ANY one permission passes
3. Public endpoints list uses startswith matching — /api/products-admin/ would bypass auth
4. Token validation doesn't check expiry
"""

from django.http import JsonResponse
from django.conf import settings


# Simulated user store (in production this would be a DB lookup)
_USERS = {
    "token-user-alice": {
        "username": "alice",
        "roles": ["viewer"],
        "permissions": ["read:products", "read:orders"],
    },
    "token-user-bob": {
        "username": "bob",
        "roles": ["editor"],
        "permissions": ["read:products", "write:products", "read:orders"],
    },
    "token-admin-carol": {
        "username": "carol",
        "roles": ["admin"],
        "permissions": ["read:products", "write:products", "read:orders",
                        "write:orders", "read:users", "write:users",
                        "admin:export"],
    },
}

# Endpoints that don't require authentication
PUBLIC_PATHS = [
    "/api/products",
    "/api/health",
]

# Endpoints that require specific permissions (RBAC)
RBAC_RULES = {
    "/api/orders/create": ["write:orders", "read:products"],
    "/api/admin/users": ["read:users", "admin:export"],
    "/api/admin/export": ["admin:export"],
    "/api/internal/metrics": [],  # Should require API key only
    "/api/internal/config": [],   # Should require API key only
}


class APIAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path.rstrip("/")

        # Skip auth for public endpoints
        # BUG 3: startswith matching is too broad —
        # /api/products-secret would match /api/products and bypass auth
        if path in PUBLIC_PATHS:
            return self.get_response(request)

        # Internal endpoints — require API key
        if path.startswith("/api/internal"):
            return self._check_api_key(request)

        # All other endpoints — require Bearer token + RBAC
        return self._check_bearer_token(request, path)

    def _check_api_key(self, request):
        api_key = request.META.get("HTTP_X_API_KEY", "")
        if not api_key or api_key != settings.INTERNAL_API_KEY:
            return JsonResponse({"error": "Invalid API key"}, status=401)
        return self.get_response(request)


    def _check_bearer_token(self, request, path):
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")

        if not auth_header.startswith("Bearer "):
            return JsonResponse(
                {"error": "Authentication required. Provide Bearer token."},
                status=401,
            )

        token = auth_header.split("Bearer ")[1]

        # BUG 4: No token expiry check — tokens are valid forever
        user = _USERS.get(token)
        if not user:
            return JsonResponse({"error": "Invalid token"}, status=401)

        # Attach user to request for downstream use
        request.api_user = user

        # Check RBAC if endpoint has rules
        if path in RBAC_RULES:
            required = RBAC_RULES[path]
            if required and not self._check_permissions(user, required):
                return JsonResponse(
                    {"error": "Insufficient permissions"},
                    status=403,
                )

        return self.get_response(request)

    def _check_permissions(self, user, required_permissions):
        user_perms = set(user.get("permissions", []))
        required = set(required_permissions)
        return required.issubset(user_perms)  # AND — all required must be present

