from rest_framework import serializers

from apps.core.models import AuditLog, Notification


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = [
            "id",
            "company",
            "user",
            "action",
            "content_type",
            "object_id",
            "old_values",
            "new_values",
            "created_at",
        ]


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "id",
            "company",
            "user",
            "message",
            "target_path",
            "target_id",
            "is_read",
            "created_at",
        ]
