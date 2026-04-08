from rest_framework import serializers
from apps.commerce.models import Product, SaleOrder, SaleOrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "company", "sku", "name", "unit_price", "is_active"]
        read_only_fields = ["company"]


class SaleOrderItemInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleOrderItem
        fields = ["product", "quantity", "unit_price"]


class SaleOrderSerializer(serializers.ModelSerializer):
    items = SaleOrderItemInputSerializer(many=True, write_only=True)

    class Meta:
        model = SaleOrder
        fields = [
            "id",
            "company",
            "customer",
            "status",
            "total_amount",
            "tax_rate",
            "currency",
            "items",
            "created_at",
        ]
        read_only_fields = ["company", "status", "total_amount", "created_at"]

    def validate(self, attrs):
        request = self.context["request"]
        company = request.company
        customer = attrs["customer"]
        if customer.company_id != company.id:
            raise serializers.ValidationError("Customer belongs to a different company.")
        for line in attrs.get("items", []):
            if line["product"].company_id != company.id:
                raise serializers.ValidationError("Products must belong to the current company.")
        return attrs

    def create(self, validated_data):
        items = validated_data.pop("items", [])
        order = SaleOrder.objects.create(company=self.context["request"].company, **validated_data)
        SaleOrderItem.objects.bulk_create(
            [SaleOrderItem(order=order, **item_data) for item_data in items]
        )
        order.recalculate_total()
        return order
