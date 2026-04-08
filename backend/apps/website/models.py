from django.db import models
from apps.core.models import CompanyOwnedModel


class WebPage(CompanyOwnedModel):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
