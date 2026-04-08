from django.db import models
from apps.core.models import CompanyOwnedModel


class Project(CompanyOwnedModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    starts_on = models.DateField(null=True, blank=True)
    ends_on = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
