from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.core.permissions import AdminOrManagerPermission, SalesPermission
from apps.core.viewsets import CompanyScopedModelViewSet
from apps.commerce.models import Product, SaleOrder
from apps.commerce.serializers import ProductSerializer, SaleOrderSerializer
from apps.commerce.services import complete_sale, refund_sale, submit_sale_for_approval


class ProductViewSet(CompanyScopedModelViewSet):
    queryset = Product.objects.all().order_by("id")
    serializer_class = ProductSerializer
    permission_classes = [SalesPermission]


class SaleOrderViewSet(CompanyScopedModelViewSet):
    queryset = SaleOrder.objects.all().order_by("-created_at")
    serializer_class = SaleOrderSerializer
    permission_classes = [SalesPermission]

    def get_permissions(self):
        if self.action == "approve":
            return [IsAuthenticated(), AdminOrManagerPermission()]
        return super().get_permissions()

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        order = self.get_object()
        order = submit_sale_for_approval(order)
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        order = self.get_object()
        try:
            order = complete_sale(order)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def refund(self, request, pk=None):
        order = self.get_object()
        amount = request.data.get("amount")
        try:
            order = refund_sale(order, amount=amount)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
