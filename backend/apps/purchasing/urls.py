from rest_framework.routers import DefaultRouter

from apps.purchasing.views import PurchaseOrderViewSet, SupplierViewSet

router = DefaultRouter()
router.register(r"suppliers", SupplierViewSet, basename="suppliers")
router.register(r"purchase-orders", PurchaseOrderViewSet, basename="purchase-orders")

urlpatterns = router.urls
