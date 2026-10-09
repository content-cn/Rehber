from django.urls import path
from . import views

urlpatterns = [
    # Public
    path("health", views.health_check, name="health"),
    path("products", views.list_products, name="list-products"),
    path("products/<int:pk>", views.get_product, name="get-product"),

    # Authenticated
    path("orders", views.list_orders, name="list-orders"),
    path("orders/create", views.create_order, name="create-order"),

    # Admin (RBAC)
    path("admin/users", views.admin_list_users, name="admin-users"),
    path("admin/export", views.admin_export_data, name="admin-export"),

    # Internal (API Key)
    path("internal/metrics", views.internal_metrics, name="internal-metrics"),
    path("internal/config", views.internal_config, name="internal-config"),
]
