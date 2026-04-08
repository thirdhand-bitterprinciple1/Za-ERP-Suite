from rest_framework import serializers

from apps.projects.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "company", "name", "description", "starts_on", "ends_on", "is_active"]
        read_only_fields = ["company"]
