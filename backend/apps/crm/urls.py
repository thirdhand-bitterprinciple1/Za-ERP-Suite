from rest_framework.routers import DefaultRouter

from apps.crm.views import LeadViewSet

router = DefaultRouter()
router.register(r"leads", LeadViewSet, basename="leads")

urlpatterns = router.urls
