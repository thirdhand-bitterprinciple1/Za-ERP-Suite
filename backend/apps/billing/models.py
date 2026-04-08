from django.db import models
from apps.core.models import CompanyOwnedModel
from apps.partners.models import Customer


class Invoice(CompanyOwnedModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        SENT = "sent", "Sent"
        PAID = "paid", "Paid"

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="invoices")
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.DRAFT)
    issue_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
