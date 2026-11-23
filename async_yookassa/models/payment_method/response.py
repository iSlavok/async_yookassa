from typing import Any

from pydantic import BaseModel

from async_yookassa.enums.payment import PaymentMethodStatus
from async_yookassa.enums.payment_methods import PaymentMethodType
from async_yookassa.models.base import ModelConfigBase
from async_yookassa.models.payment.methods.card import CardResponse
from async_yookassa.models.payment_method.confirmation import PaymentMethodConfirmationUnion
from async_yookassa.models.payment_method.holder import HolderResponse


class PaymentMethodPayerBankDetails(BaseModel):
    """Банк, через который привязан счёт СБП."""

    bank_id: str


class PaymentMethodResponse(ModelConfigBase):
    type: PaymentMethodType
    card: CardResponse | None = None
    payer_bank_details: PaymentMethodPayerBankDetails | None = None
    id: str
    saved: bool
    status: PaymentMethodStatus
    holder: HolderResponse
    title: str | None = None
    confirmation: PaymentMethodConfirmationUnion | None = None
    metadata: dict[str, Any] | None = None
