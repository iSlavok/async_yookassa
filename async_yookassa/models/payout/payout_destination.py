from typing import Annotated, Literal, Union

from pydantic import BaseModel, ConfigDict, Field, Tag

from async_yookassa.enums.payout import PayoutTypeEnum
from async_yookassa.models.base import ModelConfigBase
from async_yookassa.models.discriminator import UNKNOWN_TAG, open_discriminator
from async_yookassa.models.payment.methods.card import (
    CardBase,
    CardResponseBase,
)


class CardPayoutDestination(ModelConfigBase):
    type: Literal[PayoutTypeEnum.bank_card]
    card: CardResponseBase | None = None


class CardPayoutDestinationRequest(ModelConfigBase):
    type: Literal[PayoutTypeEnum.bank_card]
    card: CardBase


class SBPPayoutDestinationRequest(ModelConfigBase):
    type: Literal[PayoutTypeEnum.sbp]
    bank_id: str
    phone: str


class SBPPayoutDestination(SBPPayoutDestinationRequest):
    sbp_operation_id: str | None = None
    recipient_checked: bool


class YooMoneyPayoutDestination(ModelConfigBase):
    type: Literal[PayoutTypeEnum.yoo_money]
    account_number: str = Field(min_length=11, max_length=33)


class UnknownPayoutDestination(BaseModel):
    """Способ выплаты, которого эта версия библиотеки ещё не знает."""

    type: str

    model_config = ConfigDict(extra="allow")


PayoutDestinationUnion = Annotated[
    Union[
        Annotated[CardPayoutDestination, Tag("CardPayoutDestination")],
        Annotated[SBPPayoutDestination, Tag("SBPPayoutDestination")],
        Annotated[YooMoneyPayoutDestination, Tag("YooMoneyPayoutDestination")],
        Annotated[UnknownPayoutDestination, Tag(UNKNOWN_TAG)],
    ],
    open_discriminator("type", CardPayoutDestination, SBPPayoutDestination, YooMoneyPayoutDestination),
]
PayoutDestinationRequestUnion = Annotated[
    Union[CardPayoutDestinationRequest, SBPPayoutDestinationRequest, YooMoneyPayoutDestination],
    Field(discriminator="type"),
]
