from rest_framework.routers import DefaultRouter

from apps.reports.views import ReportJobViewSet

router = DefaultRouter()
router.register(r"jobs", ReportJobViewSet, basename="report-jobs")

urlpatterns = router.urls
