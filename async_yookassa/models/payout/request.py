from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

from async_yookassa.models.list_options_base import ListOptionsBase
from async_yookassa.models.payment.amount import Amount
from async_yookassa.models.payment.deal import DealBase
from async_yookassa.models.payout.payout_destination import PayoutDestinationRequestUnion
from async_yookassa.models.payout.response import PayoutResponse


class PersonalDataId(BaseModel):
    id: str


class PayoutRequest(BaseModel):
    amount: Amount
    payout_destination_data: PayoutDestinationRequestUnion | None = None
    payout_token: str | None = None
    payment_method_id: str | None = None
    description: str | None = Field(max_length=128, default=None)
    deal: DealBase | None = None
    personal_data: list[PersonalDataId] | None = None
    metadata: dict[str, Any] | None = None


class PayoutListOptions(ListOptionsBase):
    succeeded_at_gte: datetime | None = Field(default=None, serialization_alias="succeeded_at.gte")
    succeeded_at_gt: datetime | None = Field(default=None, serialization_alias="succeeded_at.gt")
    succeeded_at_lte: datetime | None = Field(default=None, serialization_alias="succeeded_at.lte")
    succeeded_at_lt: datetime | None = Field(default=None, serialization_alias="succeeded_at.lt")
    payout_destination_type: str | None = Field(default=None, serialization_alias="payout_destination.type")
    status: Literal["pending", "succeeded", "canceled"] | None = None


class PayoutSearchOptions(ListOptionsBase):
    metadata: dict[str, Any] | None = None


class PayoutListResponse(BaseModel):
    type: str
    items: list[PayoutResponse]
    next_cursor: str | None = None
