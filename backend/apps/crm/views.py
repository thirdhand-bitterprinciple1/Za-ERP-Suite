from apps.core.permissions import SalesPermission
from apps.core.viewsets import CompanyScopedModelViewSet
from apps.crm.models import Lead
from apps.crm.serializers import LeadSerializer


class LeadViewSet(CompanyScopedModelViewSet):
    queryset = Lead.objects.select_related("customer").all().order_by("-created_at")
    serializer_class = LeadSerializer
    permission_classes = [SalesPermission]
