from rest_framework import serializers

from apps.reports.models import ReportJob


class ReportJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportJob
        fields = [
            "id",
            "company",
            "report_type",
            "year",
            "month",
            "requested_by",
            "status",
            "file_path",
            "error_message",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["company", "requested_by", "status", "file_path", "error_message", "created_at", "updated_at"]
