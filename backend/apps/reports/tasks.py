from pathlib import Path
from decimal import Decimal

from celery import shared_task
from django.conf import settings
from django.db.models import Sum
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from apps.accounting.models import JournalEntry
from apps.core.models import Notification
from apps.reports.models import ReportJob


@shared_task(bind=True)
def generate_monthly_profit_and_loss_report(self, report_job_id: int) -> None:
    report_job = ReportJob.objects.select_related("company", "requested_by").get(id=report_job_id)
    report_job.status = ReportJob.Status.RUNNING
    report_job.save(update_fields=["status", "updated_at"])

    try:
        entries = JournalEntry.objects.filter(
            company=report_job.company,
            created_at__year=report_job.year,
            created_at__month=report_job.month,
        )

        revenue_total = entries.filter(credit_account="sales_revenue").aggregate(total=Sum("amount"))["total"] or Decimal("0")
        refund_total = entries.filter(is_refund=True).aggregate(total=Sum("amount"))["total"] or Decimal("0")
        tax_total = entries.filter(entry_type=JournalEntry.EntryType.TAX).aggregate(total=Sum("amount"))["total"] or Decimal("0")
        net_profit = revenue_total - refund_total - tax_total

        reports_dir = Path(settings.BASE_DIR) / "generated_reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        filename = f"pnl_{report_job.company_id}_{report_job.year}_{report_job.month}_{report_job.id}.pdf"
        file_path = reports_dir / filename

        pdf = canvas.Canvas(str(file_path), pagesize=A4)
        pdf.setTitle("Monthly Profit and Loss")
        y = 800
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, y, "ZA ERP - Monthly Profit & Loss Report")
        y -= 28
        pdf.setFont("Helvetica", 11)
        pdf.drawString(50, y, f"Company: {report_job.company.name}")
        y -= 18
        pdf.drawString(50, y, f"Period: {report_job.year}-{report_job.month:02d}")
        y -= 30
        pdf.drawString(50, y, f"Revenue: {revenue_total}")
        y -= 18
        pdf.drawString(50, y, f"Refunds: {refund_total}")
        y -= 18
        pdf.drawString(50, y, f"Tax: {tax_total}")
        y -= 18
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y, f"Net Profit: {net_profit}")
        pdf.showPage()
        pdf.save()

        report_job.status = ReportJob.Status.COMPLETED
        report_job.file_path = str(file_path)
        report_job.error_message = ""
        report_job.save(update_fields=["status", "file_path", "error_message", "updated_at"])

        Notification.objects.create(
            company=report_job.company,
            user=report_job.requested_by,
            message=f"Monthly P&L report is ready: {filename}",
            target_path="/reports",
            target_id=str(report_job.id),
        )
    except Exception as exc:
        report_job.status = ReportJob.Status.FAILED
        report_job.error_message = str(exc)
        report_job.save(update_fields=["status", "error_message", "updated_at"])
        Notification.objects.create(
            company=report_job.company,
            user=report_job.requested_by,
            message=f"Monthly P&L report failed: {exc}",
            target_path="/reports",
            target_id=str(report_job.id),
        )
        raise
