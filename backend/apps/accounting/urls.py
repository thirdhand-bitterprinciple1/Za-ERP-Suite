from rest_framework.routers import DefaultRouter
from apps.accounting.views import AccountingPolicyViewSet, CurrencyRateViewSet, JournalEntryViewSet

router = DefaultRouter()
router.register(r"currency-rates", CurrencyRateViewSet, basename="currency-rates")
router.register(r"policies", AccountingPolicyViewSet, basename="policies")
router.register(r"journal-entries", JournalEntryViewSet, basename="journal-entries")

urlpatterns = router.urls
