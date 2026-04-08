from django.db import models
from apps.core.models import CompanyOwnedModel


class Employee(CompanyOwnedModel):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField()
    title = models.CharField(max_length=128, blank=True)
    hire_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("company", "email")

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()
