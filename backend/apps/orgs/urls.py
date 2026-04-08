from rest_framework.routers import DefaultRouter
from apps.orgs.views import CompanyViewSet, MembershipViewSet

router = DefaultRouter()
router.register(r"companies", CompanyViewSet, basename="companies")
router.register(r"memberships", MembershipViewSet, basename="memberships")

urlpatterns = router.urls
