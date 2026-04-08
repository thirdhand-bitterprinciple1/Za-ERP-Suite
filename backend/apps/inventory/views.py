from decimal import Decimal
from django.db import transaction
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.permissions import InventoryPermission
from apps.core.viewsets import CompanyScopedModelViewSet
from apps.inventory.models import StockItem, StockMovement, Warehouse, WarehouseTransfer
from apps.inventory.serializers import (
    StockItemSerializer,
    StockMovementSerializer,
    WarehouseSerializer,
    WarehouseTransferSerializer,
)


class WarehouseViewSet(CompanyScopedModelViewSet):
    queryset = Warehouse.objects.all().order_by("name")
    serializer_class = WarehouseSerializer
    permission_classes = [InventoryPermission]


class StockItemViewSet(CompanyScopedModelViewSet):
    queryset = StockItem.objects.select_related("product").all().order_by("id")
    serializer_class = StockItemSerializer
    permission_classes = [InventoryPermission]


class StockMovementViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = StockMovement.objects.select_related("product").all().order_by("-created_at")
    serializer_class = StockMovementSerializer
    permission_classes = [InventoryPermission]

    def get_queryset(self):
        return super().get_queryset().filter(company=self.request.company)


class WarehouseTransferViewSet(CompanyScopedModelViewSet):
    queryset = WarehouseTransfer.objects.select_related("from_warehouse", "to_warehouse", "product").all().order_by("-created_at")
    serializer_class = WarehouseTransferSerializer
    permission_classes = [InventoryPermission]

    @transaction.atomic
    @action(detail=True, methods=["post"])
    def execute(self, request, pk=None):
        transfer = self.get_object()
        if transfer.status == WarehouseTransfer.Status.DONE:
            return Response(self.get_serializer(transfer).data, status=status.HTTP_200_OK)

        source_stock, _ = StockItem.objects.select_for_update().get_or_create(
            company=request.company,
            product=transfer.product,
            warehouse=transfer.from_warehouse,
        )
        target_stock, _ = StockItem.objects.select_for_update().get_or_create(
            company=request.company,
            product=transfer.product,
            warehouse=transfer.to_warehouse,
        )

        qty = Decimal(transfer.quantity)
        source_stock.quantity_on_hand = source_stock.quantity_on_hand - qty
        target_stock.quantity_on_hand = target_stock.quantity_on_hand + qty
        source_stock.save(update_fields=["quantity_on_hand"])
        target_stock.save(update_fields=["quantity_on_hand"])

        StockMovement.objects.create(
            company=request.company,
            product=transfer.product,
            warehouse=transfer.from_warehouse,
            movement_type=StockMovement.MovementType.OUT,
            quantity=qty,
            reference=f"transfer:{transfer.id}:out",
        )
        StockMovement.objects.create(
            company=request.company,
            product=transfer.product,
            warehouse=transfer.to_warehouse,
            movement_type=StockMovement.MovementType.IN,
            quantity=qty,
            reference=f"transfer:{transfer.id}:in",
        )
        transfer.status = WarehouseTransfer.Status.DONE
        transfer.save(update_fields=["status"])
        return Response(self.get_serializer(transfer).data, status=status.HTTP_200_OK)
