from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("auth/token/", obtain_auth_token),
    path("core/", include("apps.core.urls")),
    path("orgs/", include("apps.orgs.urls")),
    path("crm/", include("apps.crm.urls")),
    path("commerce/", include("apps.commerce.urls")),
    path("inventory/", include("apps.inventory.urls")),
    path("accounting/", include("apps.accounting.urls")),
    path("reports/", include("apps.reports.urls")),
    path("purchasing/", include("apps.purchasing.urls")),
    path("billing/", include("apps.billing.urls")),
    path("projects/", include("apps.projects.urls")),
    path("hr/", include("apps.hr.urls")),
]
