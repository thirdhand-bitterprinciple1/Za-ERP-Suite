from rest_framework import mixins, viewsets
from apps.accounting.models import AccountingPolicy, CurrencyRate, JournalEntry
from apps.accounting.serializers import (
    AccountingPolicySerializer,
    CurrencyRateSerializer,
    JournalEntrySerializer,
)
from apps.core.permissions import AccountingPermission
from apps.core.viewsets import CompanyScopedModelViewSet


class CurrencyRateViewSet(CompanyScopedModelViewSet):
    queryset = CurrencyRate.objects.all().order_by("-as_of_date")
    serializer_class = CurrencyRateSerializer
    permission_classes = [AccountingPermission]


class AccountingPolicyViewSet(CompanyScopedModelViewSet):
    queryset = AccountingPolicy.objects.all().order_by("id")
    serializer_class = AccountingPolicySerializer
    permission_classes = [AccountingPermission]


class JournalEntryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = JournalEntry.objects.all().order_by("-created_at")
    serializer_class = JournalEntrySerializer
    permission_classes = [AccountingPermission]

    def get_queryset(self):
        return super().get_queryset().filter(company=self.request.company)
