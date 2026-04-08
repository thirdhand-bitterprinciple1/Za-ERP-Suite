from django.db import models
from apps.core.models import CompanyOwnedModel


class Customer(CompanyOwnedModel):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=64, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("company", "email")

    def __str__(self) -> str:
        return self.name
