from django.db import models
from apps.commerce.models import Product
from apps.core.models import CompanyOwnedModel


class Warehouse(CompanyOwnedModel):
    code = models.CharField(max_length=32)
    name = models.CharField(max_length=255)

    class Meta:
        unique_together = ("company", "code")


class StockItem(CompanyOwnedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stock_items")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name="stock_items", null=True, blank=True)
    quantity_on_hand = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    reorder_level = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        unique_together = ("company", "product", "warehouse")


class StockMovement(CompanyOwnedModel):
    class MovementType(models.TextChoices):
        IN = "in", "Stock In"
        OUT = "out", "Stock Out"

    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="stock_movements")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name="stock_movements", null=True, blank=True)
    movement_type = models.CharField(max_length=8, choices=MovementType.choices)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    reference = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)


class WarehouseTransfer(CompanyOwnedModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        DONE = "done", "Done"

    from_warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name="outbound_transfers")
    to_warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name="inbound_transfers")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="warehouse_transfers")
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
