from rest_framework import serializers
from apps.inventory.models import StockItem, StockMovement, Warehouse, WarehouseTransfer


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ["id", "company", "code", "name"]
        read_only_fields = ["company"]


class StockItemSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        request = self.context["request"]
        company = request.company
        product = attrs.get("product")
        warehouse = attrs.get("warehouse")
        if product and product.company_id != company.id:
            raise serializers.ValidationError("Product belongs to a different company.")
        if warehouse and warehouse.company_id != company.id:
            raise serializers.ValidationError("Warehouse belongs to a different company.")
        return attrs

    class Meta:
        model = StockItem
        fields = ["id", "company", "product", "warehouse", "quantity_on_hand", "reorder_level"]
        read_only_fields = ["company"]


class StockMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = [
            "id",
            "company",
            "product",
            "warehouse",
            "movement_type",
            "quantity",
            "reference",
            "created_at",
        ]


class WarehouseTransferSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        request = self.context["request"]
        company = request.company
        from_warehouse = attrs["from_warehouse"]
        to_warehouse = attrs["to_warehouse"]
        product = attrs["product"]

        if from_warehouse.company_id != company.id or to_warehouse.company_id != company.id:
            raise serializers.ValidationError("Warehouses must belong to the current company.")
        if product.company_id != company.id:
            raise serializers.ValidationError("Product belongs to a different company.")
        if from_warehouse.id == to_warehouse.id:
            raise serializers.ValidationError("Source and destination warehouses must differ.")
        return attrs

    class Meta:
        model = WarehouseTransfer
        fields = [
            "id",
            "company",
            "from_warehouse",
            "to_warehouse",
            "product",
            "quantity",
            "status",
            "created_at",
        ]
        read_only_fields = ["company", "status", "created_at"]
