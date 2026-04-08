from django.db import transaction

from apps.core.event_bus import publish
from apps.purchasing.models import PurchaseOrder


@transaction.atomic
def receive_purchase_order(po: PurchaseOrder) -> PurchaseOrder:
    if po.status == PurchaseOrder.Status.COMPLETED:
        return po

    if po.status != PurchaseOrder.Status.PENDING_APPROVAL:
        raise ValueError("Purchase order must be pending approval before completion.")

    po.status = PurchaseOrder.Status.COMPLETED
    po.save(update_fields=["status", "updated_at"])

    publish(
        "purchase.received",
        {
            "company_id": po.company_id,
            "purchase_order_id": po.id,
            "lines": [
                {
                    "product_id": line.product_id,
                    "quantity": str(line.quantity),
                }
                for line in po.items.all()
            ],
        },
    )
    return po


@transaction.atomic
def submit_purchase_for_approval(po: PurchaseOrder) -> PurchaseOrder:
    if po.status != PurchaseOrder.Status.DRAFT:
        return po
    po.status = PurchaseOrder.Status.PENDING_APPROVAL
    po.save(update_fields=["status", "updated_at"])
    return po
