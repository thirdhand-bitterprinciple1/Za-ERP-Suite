from rest_framework import serializers
from apps.orgs.models import Company, Membership


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name", "base_currency", "is_active"]


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ["id", "user", "company", "role", "is_active"]
