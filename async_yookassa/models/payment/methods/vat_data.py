from typing import Annotated, Literal, Union

from pydantic import BaseModel, ConfigDict, Tag

from async_yookassa.enums.vat_data import RateEnum, VatDataTypeEnum
from async_yookassa.models.base import ModelConfigBase
from async_yookassa.models.discriminator import UNKNOWN_TAG, open_discriminator
from async_yookassa.models.payment.amount import Amount


class UntaxedVatData(ModelConfigBase):
    type: Literal[VatDataTypeEnum.untaxed]


class MixedVatData(ModelConfigBase):
    type: Literal[VatDataTypeEnum.mixed]
    amount: Amount


class CalculatedVatData(MixedVatData):
    type: Literal[VatDataTypeEnum.calculated]
    rate: RateEnum


class UnknownVatData(BaseModel):
    """Вид данных об НДС, которого эта версия библиотеки ещё не знает."""

    type: str

    model_config = ConfigDict(extra="allow")


VatDataUnion = Annotated[
    Union[
        Annotated[UntaxedVatData, Tag("UntaxedVatData")],
        Annotated[MixedVatData, Tag("MixedVatData")],
        Annotated[CalculatedVatData, Tag("CalculatedVatData")],
        Annotated[UnknownVatData, Tag(UNKNOWN_TAG)],
    ],
    open_discriminator("type", UntaxedVatData, MixedVatData, CalculatedVatData),
]
