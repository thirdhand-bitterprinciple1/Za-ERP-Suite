import json
import time

from django.http import HttpResponse, StreamingHttpResponse
from rest_framework import mixins, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.models import AuditLog, Notification
from apps.core.permissions import AdminOrManagerPermission, IsCompanyMember
from apps.core.serializers import AuditLogSerializer, NotificationSerializer
from apps.orgs.models import Membership


class AuditLogViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = AuditLogSerializer
    permission_classes = [AdminOrManagerPermission]

    def get_queryset(self):
        return AuditLog.objects.filter(company=self.request.company).order_by("-created_at")


class NotificationViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsCompanyMember]

    def get_queryset(self):
        return Notification.objects.filter(company=self.request.company, user=self.request.user).order_by("-created_at")

    @action(detail=True, methods=["post"])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        if not notification.is_read:
            notification.is_read = True
            notification.save(update_fields=["is_read"])
        return Response(self.get_serializer(notification).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def mark_all_read(self, request):
        queryset = self.get_queryset().filter(is_read=False)
        updated = queryset.update(is_read=True)
        return Response({"updated": updated}, status=status.HTTP_200_OK)


def notifications_stream(request):
    token_key = request.GET.get("token")
    company_id = request.GET.get("company_id")

    if not token_key or not company_id:
        return HttpResponse("Missing token/company_id", status=400)

    token = Token.objects.filter(key=token_key).select_related("user").first()
    if not token:
        return HttpResponse("Invalid token", status=401)

    membership_exists = Membership.objects.filter(
        user=token.user,
        company_id=company_id,
        is_active=True,
        company__is_active=True,
    ).exists()
    if not membership_exists:
        return HttpResponse("Invalid company context", status=403)

    def event_stream():
        previous_signature = None
        while True:
            notifications = list(
                Notification.objects.filter(company_id=company_id, user=token.user)
                .order_by("-created_at")[:8]
                .values("id", "message", "target_path", "target_id", "is_read", "created_at")
            )
            notifications.reverse()

            for item in notifications:
                item["created_at"] = item["created_at"].isoformat()

            signature = json.dumps(notifications, sort_keys=True)
            if signature != previous_signature:
                previous_signature = signature
                yield f"event: notifications\ndata: {signature}\n\n"
            else:
                yield "event: heartbeat\ndata: {}\n\n"
            time.sleep(5)

    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response["Cache-Control"] = "no-cache"
    response["X-Accel-Buffering"] = "no"
    return response
