from decimal import Decimal

from apps.accounting.models import AccountingPolicy, CurrencyRate, JournalEntry


def _rate_for(company_id: int, currency: str) -> Decimal:
    if not currency:
        return Decimal("1")
    latest = (
        CurrencyRate.objects.filter(company_id=company_id, currency=currency)
        .order_by("-as_of_date")
        .first()
    )
    return latest.rate_to_base if latest else Decimal("1")


def _policy_for(company_id: int) -> AccountingPolicy:
    policy, _ = AccountingPolicy.objects.get_or_create(company_id=company_id)
    return policy


def post_sale(company_id: int, order_id: int, total_amount: Decimal, currency: str, tax_rate: Decimal) -> None:
    policy = _policy_for(company_id)
    fx_rate = _rate_for(company_id, currency)
    gross_base = total_amount * fx_rate
    tax_amount = gross_base * (tax_rate / Decimal("100"))
    net_amount = gross_base - tax_amount

    JournalEntry.objects.create(
        company_id=company_id,
        reference=f"sale:{order_id}",
        description="Revenue from completed sale",
        debit_account=policy.accounts_receivable_account,
        credit_account=policy.sales_revenue_account,
        amount=net_amount,
        net_amount=net_amount,
        tax_amount=tax_amount,
        gross_amount=gross_base,
        source_currency=currency,
        base_currency="USD",
        fx_rate=fx_rate,
        entry_type=JournalEntry.EntryType.SALE,
    )

    if tax_amount > 0:
        JournalEntry.objects.create(
            company_id=company_id,
            reference=f"sale-tax:{order_id}",
            description="Tax recognized from sale",
            debit_account=policy.accounts_receivable_account,
            credit_account=policy.tax_liability_account,
            amount=tax_amount,
            net_amount=Decimal("0"),
            tax_amount=tax_amount,
            gross_amount=tax_amount,
            source_currency=currency,
            base_currency="USD",
            fx_rate=fx_rate,
            entry_type=JournalEntry.EntryType.TAX,
        )


def post_refund(company_id: int, order_id: int, refund_amount: Decimal, currency: str, tax_rate: Decimal) -> None:
    policy = _policy_for(company_id)
    fx_rate = _rate_for(company_id, currency)
    gross_base = refund_amount * fx_rate
    tax_amount = gross_base * (tax_rate / Decimal("100"))
    net_amount = gross_base - tax_amount

    JournalEntry.objects.create(
        company_id=company_id,
        reference=f"refund:{order_id}",
        description="Refund issued for sale",
        debit_account=policy.refund_expense_account,
        credit_account=policy.accounts_receivable_account,
        amount=net_amount,
        net_amount=net_amount,
        tax_amount=tax_amount,
        gross_amount=gross_base,
        source_currency=currency,
        base_currency="USD",
        fx_rate=fx_rate,
        entry_type=JournalEntry.EntryType.REFUND,
        is_refund=True,
    )
