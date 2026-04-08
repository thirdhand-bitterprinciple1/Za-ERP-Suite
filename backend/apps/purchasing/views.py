from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.core.permissions import AdminOrManagerPermission, PurchasingPermission
from apps.core.viewsets import CompanyScopedModelViewSet
from apps.purchasing.models import PurchaseOrder, Supplier
from apps.purchasing.serializers import PurchaseOrderSerializer, SupplierSerializer
from apps.purchasing.services import receive_purchase_order, submit_purchase_for_approval


class SupplierViewSet(CompanyScopedModelViewSet):
    queryset = Supplier.objects.all().order_by("name")
    serializer_class = SupplierSerializer
    permission_classes = [PurchasingPermission]


class PurchaseOrderViewSet(CompanyScopedModelViewSet):
    queryset = PurchaseOrder.objects.select_related("supplier").all().order_by("-created_at")
    serializer_class = PurchaseOrderSerializer
    permission_classes = [PurchasingPermission]

    def get_permissions(self):
        if self.action == "approve":
            return [IsAuthenticated(), AdminOrManagerPermission()]
        return super().get_permissions()

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        po = self.get_object()
        po = submit_purchase_for_approval(po)
        return Response(self.get_serializer(po).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        po = self.get_object()
        try:
            po = receive_purchase_order(po)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(po).data, status=status.HTTP_200_OK)
