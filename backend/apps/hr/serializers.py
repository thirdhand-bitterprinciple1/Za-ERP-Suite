from rest_framework import serializers

from apps.hr.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            "id",
            "company",
            "first_name",
            "last_name",
            "email",
            "title",
            "hire_date",
            "is_active",
        ]
        read_only_fields = ["company"]
