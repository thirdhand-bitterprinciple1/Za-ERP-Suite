from apps.accounting.handlers import handle_sale_completed, handle_sale_refunded
from apps.core.event_bus import subscribe

subscribe("sale.completed", handle_sale_completed)
subscribe("sale.refunded", handle_sale_refunded)
