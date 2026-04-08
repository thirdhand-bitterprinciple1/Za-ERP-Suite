from decimal import Decimal
import os
import secrets

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone
from rest_framework.authtoken.models import Token

from apps.accounting.models import AccountingPolicy, CurrencyRate
from apps.billing.models import Invoice
from apps.commerce.models import Product, SaleOrder, SaleOrderItem
from apps.commerce.services import complete_sale
from apps.crm.models import Lead
from apps.hr.models import Employee
from apps.inventory.models import StockItem, Warehouse, WarehouseTransfer
from apps.orgs.models import Company, Membership
from apps.partners.models import Customer
from apps.projects.models import Project
from apps.purchasing.models import PurchaseOrder, PurchaseOrderItem, Supplier
from apps.purchasing.services import receive_purchase_order


class Command(BaseCommand):
    help = "Seed demo companies, users, memberships, tokens, and starter module data."

    def add_arguments(self, parser):
        parser.add_argument(
            "--password",
            dest="password",
            default=None,
            help="Password to assign to demo users.",
        )
        parser.add_argument(
            "--reset-passwords",
            action="store_true",
            help="Reset passwords for existing demo users as well.",
        )
        parser.add_argument(
            "--rotate-tokens",
            action="store_true",
            help="Rotate auth tokens for existing demo users.",
        )

    def handle(self, *args, **options):
        user_model = get_user_model()
        reset_passwords = options["reset_passwords"]
        rotate_tokens = options["rotate_tokens"]

        company_a, _ = Company.objects.get_or_create(
            name="Acme Holdings",
            defaults={"base_currency": "USD"},
        )
        company_b, _ = Company.objects.get_or_create(
            name="Globex Trading",
            defaults={"base_currency": "EUR"},
        )

        role_specs = [
            ("admin", Membership.Role.ADMIN),
            ("manager", Membership.Role.MANAGER),
            ("sales", Membership.Role.SALES),
            ("inventory", Membership.Role.INVENTORY),
            ("accounting", Membership.Role.ACCOUNTING),
            ("purchasing", Membership.Role.PURCHASING),
            ("hr", Membership.Role.HR),
            ("projects", Membership.Role.PROJECTS),
        ]

        credentials: list[tuple[str, str, str, str, int]] = []
        default_password = options["password"] or os.getenv("DEMO_DEFAULT_PASSWORD") or secrets.token_urlsafe(12)

        for username, role in role_specs:
            email = f"{username}@acme.local"
            user, created = user_model.objects.get_or_create(
                username=username,
                defaults={"email": email},
            )
            if created or not user.has_usable_password() or reset_passwords:
                user.set_password(default_password)
                user.save(update_fields=["password"])

            Membership.objects.get_or_create(user=user, company=company_a, role=role, defaults={"is_active": True})
            if rotate_tokens:
                Token.objects.filter(user=user).delete()
            token, _ = Token.objects.get_or_create(user=user)
            credentials.append((username, default_password, role, token.key, company_a.id))

        finance_user, created = user_model.objects.get_or_create(
            username="finance_globex",
            defaults={"email": "finance@globex.local"},
        )
        if created or not finance_user.has_usable_password() or reset_passwords:
            finance_user.set_password(default_password)
            finance_user.save(update_fields=["password"])
        Membership.objects.get_or_create(
            user=finance_user,
            company=company_b,
            role=Membership.Role.ACCOUNTING,
            defaults={"is_active": True},
        )
        if rotate_tokens:
            Token.objects.filter(user=finance_user).delete()
        token, _ = Token.objects.get_or_create(user=finance_user)
        credentials.append(("finance_globex", default_password, Membership.Role.ACCOUNTING, token.key, company_b.id))

        customer, _ = Customer.objects.get_or_create(
            company=company_a,
            email="buyer@acme-client.test",
            defaults={"name": "Acme Client", "phone": "+15550123"},
        )
        product, _ = Product.objects.get_or_create(
            company=company_a,
            sku="SKU-1000",
            defaults={"name": "Starter Package", "unit_price": Decimal("199.00")},
        )

        main_wh, _ = Warehouse.objects.get_or_create(
            company=company_a,
            code="MAIN",
            defaults={"name": "Main Warehouse"},
        )
        overflow_wh, _ = Warehouse.objects.get_or_create(
            company=company_a,
            code="OVERFLOW",
            defaults={"name": "Overflow Warehouse"},
        )

        StockItem.objects.get_or_create(
            company=company_a,
            product=product,
            warehouse=main_wh,
            defaults={"quantity_on_hand": Decimal("100.00"), "reorder_level": Decimal("20.00")},
        )

        supplier, _ = Supplier.objects.get_or_create(
            company=company_a,
            name="Core Supplies Ltd",
            defaults={"email": "sales@coresupplies.test", "phone": "+15550999"},
        )
        purchase, created = PurchaseOrder.objects.get_or_create(
            company=company_a,
            supplier=supplier,
            defaults={"currency": "USD"},
        )
        if created:
            PurchaseOrderItem.objects.create(
                purchase_order=purchase,
                product=product,
                quantity=Decimal("25.00"),
                unit_price=Decimal("140.00"),
            )
            purchase.recalculate_total()
            purchase.status = PurchaseOrder.Status.PENDING_APPROVAL
            purchase.save(update_fields=["status", "updated_at"])
            receive_purchase_order(purchase)

        sale, created = SaleOrder.objects.get_or_create(
            company=company_a,
            customer=customer,
            defaults={"tax_rate": Decimal("10.00"), "currency": "USD"},
        )
        if created:
            SaleOrderItem.objects.create(
                order=sale,
                product=product,
                quantity=Decimal("2.00"),
                unit_price=Decimal("199.00"),
            )
            sale.recalculate_total()
            sale.status = SaleOrder.Status.PENDING_APPROVAL
            sale.save(update_fields=["status", "updated_at"])
            complete_sale(sale)

        WarehouseTransfer.objects.get_or_create(
            company=company_a,
            from_warehouse=main_wh,
            to_warehouse=overflow_wh,
            product=product,
            quantity=Decimal("5.00"),
            defaults={"status": WarehouseTransfer.Status.DRAFT},
        )

        Lead.objects.get_or_create(
            company=company_a,
            customer=customer,
            defaults={"source": "website", "notes": "Inbound lead from docs demo."},
        )
        Invoice.objects.get_or_create(
            company=company_a,
            customer=customer,
            defaults={
                "status": Invoice.Status.SENT,
                "issue_date": timezone.now().date(),
                "due_date": timezone.now().date(),
                "amount": Decimal("399.00"),
            },
        )
        Project.objects.get_or_create(
            company=company_a,
            name="ERP Rollout",
            defaults={"description": "Internal implementation project"},
        )
        Employee.objects.get_or_create(
            company=company_a,
            email="employee@acme.local",
            defaults={"first_name": "Demo", "last_name": "Employee", "title": "Operations Lead"},
        )

        CurrencyRate.objects.get_or_create(
            company=company_a,
            currency="USD",
            as_of_date=timezone.now().date(),
            defaults={"rate_to_base": Decimal("1.000000")},
        )
        AccountingPolicy.objects.get_or_create(company=company_a)

        self.stdout.write(self.style.SUCCESS("Seed complete. Use these demo credentials:"))
        self.stdout.write("")
        self.stdout.write("username | password | role | company_id | token")
        for username, password, role, token_key, company_id in credentials:
            self.stdout.write(f"{username} | {password} | {role} | {company_id} | {token_key}")
        self.stdout.write("")
        self.stdout.write("Required request headers:")
        self.stdout.write("Authorization: Token <token>")
        self.stdout.write("X-Company-ID: <company_id>")
