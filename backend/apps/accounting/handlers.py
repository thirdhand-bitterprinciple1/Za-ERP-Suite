from decimal import Decimal
from apps.accounting.services import post_refund, post_sale


def handle_sale_completed(payload: dict[str, str]) -> None:
    company_id = payload["company_id"]
    order_id = payload["order_id"]
    amount = Decimal(payload["total_amount"])
    currency = payload.get("currency", "USD")
    tax_rate = Decimal(payload.get("tax_rate", "0"))
    post_sale(company_id=company_id, order_id=order_id, total_amount=amount, currency=currency, tax_rate=tax_rate)


def handle_sale_refunded(payload: dict[str, str]) -> None:
    company_id = payload["company_id"]
    order_id = payload["order_id"]
    refund_amount = Decimal(payload["refund_amount"])
    currency = payload.get("currency", "USD")
    tax_rate = Decimal(payload.get("tax_rate", "0"))
    post_refund(
        company_id=company_id,
        order_id=order_id,
        refund_amount=refund_amount,
        currency=currency,
        tax_rate=tax_rate,
    )
