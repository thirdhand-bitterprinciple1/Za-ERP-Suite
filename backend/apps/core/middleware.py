from django.http import JsonResponse
from apps.orgs.models import Membership
from apps.core.context import set_current_user


class CompanyContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.company = None
        set_current_user(request.user if request.user.is_authenticated else None)
        if request.user.is_authenticated:
            company_id = request.headers.get("X-Company-ID")
            memberships = Membership.objects.filter(user=request.user, is_active=True, company__is_active=True)
            if company_id:
                membership = memberships.filter(company_id=company_id).select_related("company").first()
            else:
                membership = memberships.select_related("company").first()
            if membership:
                request.company = membership.company
            elif company_id:
                return JsonResponse({"detail": "Invalid company context."}, status=403)
        response = self.get_response(request)
        set_current_user(None)
        return response
