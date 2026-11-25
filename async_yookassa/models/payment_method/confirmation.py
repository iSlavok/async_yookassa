from typing import Annotated, Literal, Union

from pydantic import BaseModel, ConfigDict, Field, Tag

from async_yookassa.enums.payment import ConfirmationType
from async_yookassa.models.base import ModelConfigBase
from async_yookassa.models.discriminator import UNKNOWN_TAG, open_discriminator


class RedirectConfirmationResponse(ModelConfigBase):
    type: Literal[ConfirmationType.redirect]
    confirmation_url: str
    enforce: bool | None = None
    return_url: str | None = None


class QRConfirmationResponse(ModelConfigBase):
    """Привязка через СБП: пользователь сканирует QR-код в приложении банка."""

    type: Literal[ConfirmationType.qr]
    confirmation_data: str


class UnknownConfirmationResponse(BaseModel):
    """Сценарий подтверждения привязки, которого эта версия библиотеки ещё не знает."""

    type: str

    model_config = ConfigDict(extra="allow")


PaymentMethodConfirmationUnion = Annotated[
    Union[
        Annotated[RedirectConfirmationResponse, Tag("RedirectConfirmationResponse")],
        Annotated[QRConfirmationResponse, Tag("QRConfirmationResponse")],
        Annotated[UnknownConfirmationResponse, Tag(UNKNOWN_TAG)],
    ],
    open_discriminator("type", RedirectConfirmationResponse, QRConfirmationResponse),
]


class RedirectConfirmationRequest(ModelConfigBase):
    type: Literal[ConfirmationType.redirect]
    enforce: bool | None = None
    locale: str | None = None
    return_url: str


class QRConfirmationRequest(ModelConfigBase):
    type: Literal[ConfirmationType.qr]
    return_url: str | None = None


PaymentMethodConfirmationRequestUnion = Annotated[
    Union[RedirectConfirmationRequest, QRConfirmationRequest],
    Field(discriminator="type"),
]
