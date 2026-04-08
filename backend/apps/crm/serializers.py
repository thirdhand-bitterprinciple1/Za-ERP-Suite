from rest_framework import serializers

from apps.crm.models import Lead


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ["id", "company", "customer", "stage", "source", "notes", "created_at"]
        read_only_fields = ["company", "created_at"]

    def validate(self, attrs):
        request = self.context["request"]
        customer = attrs["customer"]
        if customer.company_id != request.company.id:
            raise serializers.ValidationError("Customer belongs to a different company.")
        return attrs
