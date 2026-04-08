from rest_framework import serializers

from apps.billing.models import Invoice


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = [
            "id",
            "company",
            "customer",
            "status",
            "issue_date",
            "due_date",
            "amount",
        ]
        read_only_fields = ["company"]

    def validate(self, attrs):
        request = self.context["request"]
        customer = attrs.get("customer")
        if customer and customer.company_id != request.company.id:
            raise serializers.ValidationError("Customer belongs to a different company.")
        return attrs
