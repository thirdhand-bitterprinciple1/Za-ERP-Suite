from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.core.views import AuditLogViewSet, NotificationViewSet, notifications_stream

router = DefaultRouter()
router.register(r"audit-logs", AuditLogViewSet, basename="audit-logs")
router.register(r"notifications", NotificationViewSet, basename="notifications")

urlpatterns = [
	path("notifications/stream/", notifications_stream),
]
urlpatterns += router.urls
