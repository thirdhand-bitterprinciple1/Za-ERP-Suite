from rest_framework.routers import DefaultRouter
from apps.inventory.views import (
	StockItemViewSet,
	StockMovementViewSet,
	WarehouseTransferViewSet,
	WarehouseViewSet,
)

router = DefaultRouter()
router.register(r"warehouses", WarehouseViewSet, basename="warehouses")
router.register(r"stock-items", StockItemViewSet, basename="stock-items")
router.register(r"stock-movements", StockMovementViewSet, basename="stock-movements")
router.register(r"warehouse-transfers", WarehouseTransferViewSet, basename="warehouse-transfers")

urlpatterns = router.urls
