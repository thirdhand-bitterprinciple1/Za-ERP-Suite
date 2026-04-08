from decimal import Decimal
from django.contrib.auth import get_user_model
from apps.commerce.models import Product, SaleOrder, SaleOrderItem
from apps.commerce.services import complete_sale
from apps.inventory.models import StockItem
from apps.orgs.models import Company, Membership
from apps.partners.models import Customer


def run() -> None:
    user_model = get_user_model()
    user, _ = user_model.objects.get_or_create(username="admin")
    company, _ = Company.objects.get_or_create(name="Acme Holdings", defaults={"base_currency": "USD"})
    Membership.objects.get_or_create(user=user, company=company, role=Membership.Role.ADMIN)

    customer, _ = Customer.objects.get_or_create(
        company=company,
        name="Acme Inc",
        email="ops@acme.test",
    )

    product, _ = Product.objects.get_or_create(
        company=company,
        sku="SKU-1000",
        defaults={"name": "Starter Package", "unit_price": Decimal("199.00")},
    )
    StockItem.objects.get_or_create(
        company=company,
        product=product,
        defaults={"quantity_on_hand": Decimal("50")},
    )

    order = SaleOrder.objects.create(company=company, customer=customer, tax_rate=Decimal("10.00"))
    SaleOrderItem.objects.create(
        order=order,
        product=product,
        quantity=Decimal("2"),
        unit_price=product.unit_price,
    )
    order.recalculate_total()
    complete_sale(order)
