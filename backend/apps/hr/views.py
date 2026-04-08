from apps.core.permissions import HRPermission
from apps.core.viewsets import CompanyScopedModelViewSet
from apps.hr.models import Employee
from apps.hr.serializers import EmployeeSerializer


class EmployeeViewSet(CompanyScopedModelViewSet):
    queryset = Employee.objects.all().order_by("first_name", "last_name")
    serializer_class = EmployeeSerializer
    permission_classes = [HRPermission]
