from datetime import datetime
from typing import Any

from pydantic import BaseModel

from async_yookassa.enums.payment import ReceiptRegistrationStatus
from async_yookassa.enums.status import OperationStatus
from async_yookassa.models.base import ModelConfigBase
from async_yookassa.models.payment.amount import Amount
from async_yookassa.models.payment.cancellation_details import CancellationDetails
from async_yookassa.models.payment.deal import DealRefundResponse
from async_yookassa.models.payment.methods.base import PaymentMethodRefundUnion
from async_yookassa.models.payment.transfers import TransferBase


class RefundAuthorizationDetails(ModelConfigBase):
    rrn: str | None = None


class RefundResponse(ModelConfigBase):
    id: str
    payment_id: str
    status: OperationStatus
    cancellation_details: CancellationDetails | None = None
    receipt_registration: ReceiptRegistrationStatus | None = None
    created_at: datetime
    amount: Amount
    description: str | None = None
    sources: list[TransferBase] | None = None
    deal: DealRefundResponse | None = None
    refund_method: PaymentMethodRefundUnion | None = None
    refund_authorization_details: RefundAuthorizationDetails | None = None
    metadata: dict[str, Any] | None = None


class RefundListResponse(BaseModel):
    type: str
    items: list[RefundResponse]
    next_cursor: str | None = None
