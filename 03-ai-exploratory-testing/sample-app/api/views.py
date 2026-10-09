"""API Views — endpoints for products, orders, admin, and internal operations.

This file is intentionally clean. The bugs live in the middleware layer.
The point is that views LOOK correct, but the middleware chain has gaps.
"""

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


# --- Sample data (in-memory) ---

PRODUCTS = [
    {"id": 1, "name": "Wireless Keyboard", "price": 49.99, "stock": 150},
    {"id": 2, "name": "USB-C Hub", "price": 34.99, "stock": 80},
    {"id": 3, "name": "Monitor Stand", "price": 79.99, "stock": 45},
    {"id": 4, "name": "Noise-Cancelling Headphones", "price": 199.99, "stock": 30},
]

ORDERS = [
    {"id": 1, "user": "alice", "product_id": 1, "quantity": 2, "status": "shipped"},
    {"id": 2, "user": "bob", "product_id": 3, "quantity": 1, "status": "processing"},
]

USERS_DB = [
    {"id": 1, "username": "alice", "email": "alice@example.com", "role": "viewer"},
    {"id": 2, "username": "bob", "email": "bob@example.com", "role": "editor"},
    {"id": 3, "username": "carol", "email": "carol@company.internal", "role": "admin"},
]

_next_order_id = 3


# ==================== PUBLIC ENDPOINTS ====================

def health_check(request):
    return JsonResponse({"status": "ok", "service": "demo-api", "version": "1.2.0"})


@require_http_methods(["GET"])
def list_products(request):
    return JsonResponse({"products": PRODUCTS})


@require_http_methods(["GET"])
def get_product(request, pk):
    product = next((p for p in PRODUCTS if p["id"] == pk), None)
    if not product:
        return JsonResponse({"error": "Product not found"}, status=404)
    return JsonResponse(product)


# ==================== AUTHENTICATED ENDPOINTS ====================

@require_http_methods(["GET"])
def list_orders(request):
    user = getattr(request, "api_user", None)
    if not user:
        return JsonResponse({"error": "Not authenticated"}, status=401)

    # Non-admin users only see their own orders
    if "admin" not in user.get("roles", []):
        user_orders = [o for o in ORDERS if o["user"] == user["username"]]
        return JsonResponse({"orders": user_orders})

    return JsonResponse({"orders": ORDERS})


@csrf_exempt
@require_http_methods(["POST"])
def create_order(request):
    user = getattr(request, "api_user", None)
    if not user:
        return JsonResponse({"error": "Not authenticated"}, status=401)

    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({"error": "Invalid JSON body"}, status=400)

    product_id = body.get("product_id")
    quantity = body.get("quantity", 1)

    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        return JsonResponse({"error": "Product not found"}, status=404)

    global _next_order_id
    order = {
        "id": _next_order_id,
        "user": user["username"],
        "product_id": product_id,
        "quantity": quantity,
        "status": "pending",
    }
    ORDERS.append(order)
    _next_order_id += 1

    return JsonResponse({"order": order}, status=201)


# ==================== ADMIN ENDPOINTS (RBAC) ====================

@require_http_methods(["GET"])
def admin_list_users(request):
    return JsonResponse({"users": USERS_DB})


@require_http_methods(["GET"])
def admin_export_data(request):
    """Export all data — intended for admin-only bulk exports."""
    return JsonResponse({
        "export": {
            "products": PRODUCTS,
            "orders": ORDERS,
            "users": USERS_DB,
        }
    })


# ==================== INTERNAL ENDPOINTS (API Key) ====================

def internal_metrics(request):
    return JsonResponse({
        "metrics": {
            "total_products": len(PRODUCTS),
            "total_orders": len(ORDERS),
            "total_users": len(USERS_DB),
            "api_version": "1.2.0",
        }
    })


def internal_config(request):
    """Returns internal configuration — should be strictly protected."""
    from django.conf import settings
    return JsonResponse({
        "config": {
            "debug": settings.DEBUG,
            "database": str(settings.DATABASES["default"]["ENGINE"]),
            "rate_limit": settings.RATE_LIMIT_REQUESTS,
            "rate_window": settings.RATE_LIMIT_WINDOW_SECONDS,
            "secret_key_preview": settings.SECRET_KEY[:8] + "...",
        }
    })
