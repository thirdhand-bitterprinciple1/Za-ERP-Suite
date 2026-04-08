from apps.core.permissions import ProjectsPermission
from apps.core.viewsets import CompanyScopedModelViewSet
from apps.projects.models import Project
from apps.projects.serializers import ProjectSerializer


class ProjectViewSet(CompanyScopedModelViewSet):
    queryset = Project.objects.all().order_by("name")
    serializer_class = ProjectSerializer
    permission_classes = [ProjectsPermission]
