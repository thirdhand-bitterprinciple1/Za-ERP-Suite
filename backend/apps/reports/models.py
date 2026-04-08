from django.conf import settings
from django.db import models

from apps.core.models import CompanyOwnedModel


class ReportJob(CompanyOwnedModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        RUNNING = "running", "Running"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    report_type = models.CharField(max_length=64, default="monthly_profit_and_loss")
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="report_jobs")
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
    file_path = models.CharField(max_length=512, blank=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
