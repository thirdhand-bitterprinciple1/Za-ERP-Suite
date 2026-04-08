from rest_framework.routers import DefaultRouter

from apps.hr.views import EmployeeViewSet

router = DefaultRouter()
router.register(r"employees", EmployeeViewSet, basename="employees")

urlpatterns = router.urls
