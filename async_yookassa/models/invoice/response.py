from datetime import datetime
from typing import Any

from async_yookassa.enums.status import OperationStatus
from async_yookassa.models.base import ModelConfigBase
from async_yookassa.models.invoice.cart import Cart
from async_yookassa.models.invoice.delivery_method import DeliveryMethodResponseUnion
from async_yookassa.models.invoice.invoice_cancellation_details import InvoiceCancellationDetails
from async_yookassa.models.invoice.payment_details import PaymentDetails


class InvoiceResponse(ModelConfigBase):
    id: str
    status: OperationStatus
    cart: list[Cart]
    delivery_method: DeliveryMethodResponseUnion | None = None
    payment_details: PaymentDetails | None = None
    created_at: datetime
    expires_at: datetime | None = None
    description: str | None = None
    cancellation_details: InvoiceCancellationDetails | None = None
    metadata: dict[str, Any] | None = None
