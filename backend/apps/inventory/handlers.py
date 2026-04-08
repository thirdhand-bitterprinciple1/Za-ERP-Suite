from decimal import Decimal
from django.db import transaction

from apps.inventory.models import StockItem, StockMovement


@transaction.atomic
def handle_sale_completed(payload: dict[str, str]) -> None:
    company_id = payload["company_id"]
    order_id = payload["order_id"]
    for line in payload["lines"]:
        product_id = line["product_id"]
        quantity = Decimal(line["quantity"])

        stock, _ = StockItem.objects.select_for_update().get_or_create(
            company_id=company_id,
            product_id=product_id,
        )
        stock.quantity_on_hand = stock.quantity_on_hand - quantity
        stock.save(update_fields=["quantity_on_hand"])

        StockMovement.objects.create(
            company_id=company_id,
            product_id=product_id,
            movement_type=StockMovement.MovementType.OUT,
            quantity=quantity,
            reference=f"sale:{order_id}",
        )


@transaction.atomic
def handle_sale_refunded(payload: dict[str, str]) -> None:
    company_id = payload["company_id"]
    order_id = payload["order_id"]
    for line in payload["lines"]:
        product_id = line["product_id"]
        quantity = Decimal(line["quantity"])

        stock, _ = StockItem.objects.select_for_update().get_or_create(
            company_id=company_id,
            product_id=product_id,
        )
        stock.quantity_on_hand = stock.quantity_on_hand + quantity
        stock.save(update_fields=["quantity_on_hand"])

        StockMovement.objects.create(
            company_id=company_id,
            product_id=product_id,
            movement_type=StockMovement.MovementType.IN,
            quantity=quantity,
            reference=f"refund:{order_id}",
        )


@transaction.atomic
def handle_purchase_received(payload: dict[str, str]) -> None:
    company_id = payload["company_id"]
    purchase_order_id = payload["purchase_order_id"]
    for line in payload["lines"]:
        product_id = line["product_id"]
        quantity = Decimal(line["quantity"])

        stock, _ = StockItem.objects.select_for_update().get_or_create(
            company_id=company_id,
            product_id=product_id,
        )
        stock.quantity_on_hand = stock.quantity_on_hand + quantity
        stock.save(update_fields=["quantity_on_hand"])

        StockMovement.objects.create(
            company_id=company_id,
            product_id=product_id,
            movement_type=StockMovement.MovementType.IN,
            quantity=quantity,
            reference=f"purchase:{purchase_order_id}",
        )
