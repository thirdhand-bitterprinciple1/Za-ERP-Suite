from django.db import models
from apps.core.models import CompanyOwnedModel
from apps.partners.models import Customer


class Lead(CompanyOwnedModel):
    class Stage(models.TextChoices):
        NEW = "new", "New"
        QUALIFIED = "qualified", "Qualified"
        WON = "won", "Won"
        LOST = "lost", "Lost"

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="leads")
    stage = models.CharField(max_length=16, choices=Stage.choices, default=Stage.NEW)
    source = models.CharField(max_length=128, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
