from rest_framework import serializers

from apps.purchasing.models import PurchaseOrder, PurchaseOrderItem, Supplier


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ["id", "company", "name", "email", "phone"]
        read_only_fields = ["company"]


class PurchaseOrderItemInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderItem
        fields = ["product", "quantity", "unit_price"]


class PurchaseOrderSerializer(serializers.ModelSerializer):
    items = PurchaseOrderItemInputSerializer(many=True, write_only=True)

    class Meta:
        model = PurchaseOrder
        fields = [
            "id",
            "company",
            "supplier",
            "status",
            "total_amount",
            "currency",
            "items",
            "created_at",
        ]
        read_only_fields = ["company", "status", "total_amount", "created_at"]

    def validate(self, attrs):
        request = self.context["request"]
        company = request.company
        supplier = attrs["supplier"]
        if supplier.company_id != company.id:
            raise serializers.ValidationError("Supplier belongs to a different company.")
        for line in attrs.get("items", []):
            if line["product"].company_id != company.id:
                raise serializers.ValidationError("Products must belong to the current company.")
        return attrs

    def create(self, validated_data):
        items = validated_data.pop("items", [])
        po = PurchaseOrder.objects.create(**validated_data)
        PurchaseOrderItem.objects.bulk_create(
            [PurchaseOrderItem(purchase_order=po, **item_data) for item_data in items]
        )
        po.recalculate_total()
        return po
