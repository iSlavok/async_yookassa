from typing import Annotated, Literal, Union

from pydantic import BaseModel, ConfigDict, EmailStr, Field, Tag

from async_yookassa.enums.delivery_method import DeliveryMethodType
from async_yookassa.models.base import ModelConfigBase
from async_yookassa.models.discriminator import UNKNOWN_TAG, open_discriminator


class SMSDeliveryMethod(ModelConfigBase):
    type: Literal[DeliveryMethodType.SMS]


class SMSDeliveryMethodRequest(SMSDeliveryMethod):
    phone: str


class EmailDeliveryMethod(ModelConfigBase):
    type: Literal[DeliveryMethodType.EMAIL]


class EmailDeliveryMethodRequest(EmailDeliveryMethod):
    email: EmailStr


class SelfDeliveryMethodRequest(ModelConfigBase):
    type: Literal[DeliveryMethodType.SELF]


class SelfDeliveryMethodResponse(SelfDeliveryMethodRequest):
    url: str | None = Field(max_length=2048, default=None)


class UnknownDeliveryMethod(BaseModel):
    """Способ доставки счёта, которого эта версия библиотеки ещё не знает."""

    type: str

    model_config = ConfigDict(extra="allow")


DeliveryMethodResponseUnion = Annotated[
    Union[
        Annotated[SMSDeliveryMethod, Tag("SMSDeliveryMethod")],
        Annotated[EmailDeliveryMethod, Tag("EmailDeliveryMethod")],
        Annotated[SelfDeliveryMethodResponse, Tag("SelfDeliveryMethodResponse")],
        Annotated[UnknownDeliveryMethod, Tag(UNKNOWN_TAG)],
    ],
    open_discriminator("type", SMSDeliveryMethod, EmailDeliveryMethod, SelfDeliveryMethodResponse),
]
DeliveryMethodRequestUnion = Annotated[
    Union[SMSDeliveryMethodRequest, EmailDeliveryMethodRequest, SelfDeliveryMethodRequest],
    Field(discriminator="type"),
]
