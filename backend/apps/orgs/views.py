from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from apps.orgs.models import Company, Membership
from apps.orgs.serializers import CompanySerializer, MembershipSerializer


class CompanyViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Company.objects.filter(
            memberships__user=self.request.user,
            memberships__is_active=True,
            is_active=True,
        ).distinct().order_by("name")


class MembershipViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = MembershipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Membership.objects.filter(user=self.request.user, is_active=True).select_related("company")
