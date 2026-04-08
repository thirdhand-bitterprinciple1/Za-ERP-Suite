from django.db import models
from apps.core.models import CompanyOwnedModel


class CurrencyRate(CompanyOwnedModel):
    currency = models.CharField(max_length=3)
    rate_to_base = models.DecimalField(max_digits=14, decimal_places=6)
    as_of_date = models.DateField()

    class Meta:
        unique_together = ("company", "currency", "as_of_date")


class AccountingPolicy(CompanyOwnedModel):
    sales_revenue_account = models.CharField(max_length=64, default="sales_revenue")
    accounts_receivable_account = models.CharField(max_length=64, default="accounts_receivable")
    tax_liability_account = models.CharField(max_length=64, default="tax_liability")
    refund_expense_account = models.CharField(max_length=64, default="refunds")
    default_tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)


class JournalEntry(CompanyOwnedModel):
    class EntryType(models.TextChoices):
        SALE = "sale", "Sale"
        TAX = "tax", "Tax"
        REFUND = "refund", "Refund"

    reference = models.CharField(max_length=128)
    description = models.CharField(max_length=255)
    debit_account = models.CharField(max_length=64)
    credit_account = models.CharField(max_length=64)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    net_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    gross_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    source_currency = models.CharField(max_length=3, default="USD")
    base_currency = models.CharField(max_length=3, default="USD")
    fx_rate = models.DecimalField(max_digits=14, decimal_places=6, default=1)
    entry_type = models.CharField(max_length=16, choices=EntryType.choices, default=EntryType.SALE)
    is_refund = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
