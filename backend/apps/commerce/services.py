from django.db import transaction
from decimal import Decimal
from apps.commerce.models import SaleOrder
from apps.core.event_bus import publish


@transaction.atomic
def complete_sale(order: SaleOrder) -> SaleOrder:
    if order.status == SaleOrder.Status.COMPLETED:
        return order

    if order.status != SaleOrder.Status.PENDING_APPROVAL:
        raise ValueError("Sale order must be pending approval before completion.")

    order.status = SaleOrder.Status.COMPLETED
    order.save(update_fields=["status", "updated_at"])

    payload = {
        "company_id": order.company_id,
        "order_id": order.id,
        "customer_id": order.customer_id,
        "total_amount": str(order.total_amount),
        "tax_rate": str(order.tax_rate),
        "currency": order.currency,
        "lines": [
            {
                "product_id": item.product_id,
                "quantity": str(item.quantity),
                "unit_price": str(item.unit_price),
            }
            for item in order.items.all()
        ],
    }
    publish("sale.completed", payload)
    return order


@transaction.atomic
def refund_sale(order: SaleOrder, amount: str | None = None) -> SaleOrder:
    if order.status != SaleOrder.Status.COMPLETED:
        raise ValueError("Only completed orders can be refunded.")
    refund_amount = Decimal(amount) if amount else order.total_amount
    payload = {
        "company_id": order.company_id,
        "order_id": order.id,
        "currency": order.currency,
        "refund_amount": str(refund_amount),
        "tax_rate": str(order.tax_rate),
        "lines": [
            {
                "product_id": item.product_id,
                "quantity": str(item.quantity),
                "unit_price": str(item.unit_price),
            }
            for item in order.items.all()
        ],
    }
    publish("sale.refunded", payload)
    return order


@transaction.atomic
def submit_sale_for_approval(order: SaleOrder) -> SaleOrder:
    if order.status != SaleOrder.Status.DRAFT:
        return order
    order.status = SaleOrder.Status.PENDING_APPROVAL
    order.save(update_fields=["status", "updated_at"])
    return order
