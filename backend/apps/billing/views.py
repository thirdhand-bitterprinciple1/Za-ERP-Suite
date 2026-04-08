from apps.billing.models import Invoice
from apps.billing.serializers import InvoiceSerializer
from apps.core.permissions import BillingPermission
from apps.core.viewsets import CompanyScopedModelViewSet


class InvoiceViewSet(CompanyScopedModelViewSet):
    queryset = Invoice.objects.select_related("customer").all().order_by("-id")
    serializer_class = InvoiceSerializer
    permission_classes = [BillingPermission]
