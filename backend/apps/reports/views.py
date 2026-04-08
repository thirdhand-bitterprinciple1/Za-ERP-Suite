from pathlib import Path

from django.conf import settings
from django.http import FileResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.permissions import AccountingPermission
from apps.core.viewsets import CompanyScopedModelViewSet
from apps.reports.models import ReportJob
from apps.reports.serializers import ReportJobSerializer
from apps.reports.tasks import generate_monthly_profit_and_loss_report


class ReportJobViewSet(CompanyScopedModelViewSet):
    queryset = ReportJob.objects.select_related("requested_by").all().order_by("-created_at")
    serializer_class = ReportJobSerializer
    permission_classes = [AccountingPermission]

    def perform_create(self, serializer):
        job = serializer.save(company=self.request.company, requested_by=self.request.user)
        generate_monthly_profit_and_loss_report.delay(job.id)

    @action(detail=True, methods=["post"])
    def rerun(self, request, pk=None):
        job = self.get_object()
        generate_monthly_profit_and_loss_report.delay(job.id)
        return Response(self.get_serializer(job).data, status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=["get"])
    def download(self, request, pk=None):
        job = self.get_object()
        if job.status != ReportJob.Status.COMPLETED or not job.file_path:
            return Response({"detail": "Report file is not ready yet."}, status=status.HTTP_400_BAD_REQUEST)

        file_path = Path(job.file_path).resolve()
        allowed_dir = (Path(settings.BASE_DIR) / "generated_reports").resolve()
        if allowed_dir not in file_path.parents:
            return Response({"detail": "Invalid report path."}, status=status.HTTP_400_BAD_REQUEST)
        if not file_path.exists():
            return Response({"detail": "Report file not found."}, status=status.HTTP_404_NOT_FOUND)

        return FileResponse(open(file_path, "rb"), as_attachment=True, filename=file_path.name)
