from rest_framework import serializers
from apps.accounting.models import AccountingPolicy, CurrencyRate, JournalEntry


class CurrencyRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyRate
        fields = ["id", "company", "currency", "rate_to_base", "as_of_date"]
        read_only_fields = ["company"]


class AccountingPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountingPolicy
        fields = [
            "id",
            "company",
            "sales_revenue_account",
            "accounts_receivable_account",
            "tax_liability_account",
            "refund_expense_account",
            "default_tax_rate",
        ]
        read_only_fields = ["company"]


class JournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = [
            "id",
            "company",
            "reference",
            "description",
            "debit_account",
            "credit_account",
            "amount",
            "net_amount",
            "tax_amount",
            "gross_amount",
            "source_currency",
            "base_currency",
            "fx_rate",
            "entry_type",
            "is_refund",
            "created_at",
        ]
