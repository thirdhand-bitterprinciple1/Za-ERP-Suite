from apps.core.event_bus import subscribe
from apps.inventory.handlers import handle_purchase_received, handle_sale_completed, handle_sale_refunded

subscribe("sale.completed", handle_sale_completed)
subscribe("sale.refunded", handle_sale_refunded)
subscribe("purchase.received", handle_purchase_received)
