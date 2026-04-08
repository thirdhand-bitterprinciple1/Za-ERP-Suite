from decimal import Decimal
from django.db import models
from apps.core.models import CompanyOwnedModel
from apps.partners.models import Customer


class Product(CompanyOwnedModel):
    sku = models.CharField(max_length=64)
    name = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("company", "sku")

    def __str__(self) -> str:
        return f"{self.sku} - {self.name}"


class SaleOrder(CompanyOwnedModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PENDING_APPROVAL = "pending_approval", "Pending Approval"
        COMPLETED = "completed", "Completed"

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="sale_orders")
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.DRAFT)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default="USD")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def recalculate_total(self) -> Decimal:
        total = sum((item.quantity * item.unit_price for item in self.items.all()), Decimal("0.00"))
        self.total_amount = total
        self.save(update_fields=["total_amount", "updated_at"])
        return total


class SaleOrderItem(models.Model):
    order = models.ForeignKey(SaleOrder, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="order_items")
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)

    def line_total(self) -> Decimal:
        return self.quantity * self.unit_price
