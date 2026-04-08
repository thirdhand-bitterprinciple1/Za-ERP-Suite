from django.conf import settings
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    base_currency = models.CharField(max_length=3, default="USD")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class Membership(models.Model):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        MANAGER = "manager", "Manager"
        SALES = "sales", "Sales"
        INVENTORY = "inventory", "Inventory"
        ACCOUNTING = "accounting", "Accounting"
        HR = "hr", "HR"
        PROJECTS = "projects", "Projects"
        PURCHASING = "purchasing", "Purchasing"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="memberships")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="memberships")
    role = models.CharField(max_length=24, choices=Role.choices)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("user", "company", "role")
