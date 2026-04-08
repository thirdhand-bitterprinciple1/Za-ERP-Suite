from rest_framework.routers import DefaultRouter
from apps.commerce.views import ProductViewSet, SaleOrderViewSet

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="products")
router.register(r"orders", SaleOrderViewSet, basename="orders")

urlpatterns = router.urls
