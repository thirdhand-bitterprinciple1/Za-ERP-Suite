from rest_framework.permissions import BasePermission
from apps.orgs.models import Membership


class IsCompanyMember(BasePermission):
    def has_permission(self, request, view):
        company = getattr(request, "company", None)
        return bool(request.user and request.user.is_authenticated and company)


class AdminOrManagerPermission(BasePermission):
    def has_permission(self, request, view):
        company = getattr(request, "company", None)
        if not (request.user and request.user.is_authenticated and company):
            return False
        role_set = set(
            Membership.objects.filter(user=request.user, company=company, is_active=True).values_list("role", flat=True)
        )
        return Membership.Role.ADMIN in role_set or Membership.Role.MANAGER in role_set


class ModuleRolePermission(BasePermission):
    allowed_roles: tuple[str, ...] = tuple()

    def has_permission(self, request, view):
        company = getattr(request, "company", None)
        if not (request.user and request.user.is_authenticated and company):
            return False

        role_set = set(
            Membership.objects.filter(user=request.user, company=company, is_active=True).values_list("role", flat=True)
        )
        if Membership.Role.ADMIN in role_set:
            return True
        return any(role in role_set for role in self.allowed_roles)


class SalesPermission(ModuleRolePermission):
    allowed_roles = (Membership.Role.SALES,)


class InventoryPermission(ModuleRolePermission):
    allowed_roles = (Membership.Role.INVENTORY, Membership.Role.PURCHASING)


class AccountingPermission(ModuleRolePermission):
    allowed_roles = (Membership.Role.ACCOUNTING,)


class PurchasingPermission(ModuleRolePermission):
    allowed_roles = (Membership.Role.PURCHASING,)


class HRPermission(ModuleRolePermission):
    allowed_roles = (Membership.Role.HR,)


class ProjectsPermission(ModuleRolePermission):
    allowed_roles = (Membership.Role.PROJECTS,)


class BillingPermission(ModuleRolePermission):
    allowed_roles = (Membership.Role.ACCOUNTING, Membership.Role.SALES)
