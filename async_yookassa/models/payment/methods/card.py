import re

from pydantic import BaseModel, field_validator

from async_yookassa.enums.payment import CardSource, CardType
from async_yookassa.models.base import ModelConfigBase
from async_yookassa.models.payment.methods.card_product import (
    CardProduct,
)


def _check(pattern: str, value: object, message: str) -> str:
    if not isinstance(value, str) or not re.match(pattern, value):
        raise ValueError(message)
    return value


class CardBase(BaseModel):
    number: str

    @field_validator("number", mode="before")
    def validate_number(cls, value: object) -> str:
        return _check("^[0-9]{14,19}$", value, "Invalid card number value")


class CardRequest(CardBase):
    expiry_year: str
    expiry_month: str
    cardholder: str | None = None
    csc: str | None = None

    @field_validator("expiry_year", mode="before")
    def validate_expiry_year(cls, value: object) -> str:
        return _check("^[0-9]{4}$", value, "Invalid expiry year value")

    @field_validator("expiry_month", mode="before")
    def validate_expiry_month(cls, value: object) -> str:
        if not isinstance(value, str) or not re.match("^[0-9]{2}$", value) or not 1 <= int(value) <= 12:
            raise ValueError("Invalid expiry month value")

        return value

    @field_validator("cardholder", mode="before")
    def validate_cardholder(cls, value: object) -> str | None:
        if value is None:
            return None

        return _check("^[a-zA-Z '-]{0,26}$", value, "Invalid cardholder value")

    @field_validator("csc", mode="before")
    def validate_csc(cls, value: object) -> str | None:
        if value is None:
            return None

        return _check("^[0-9]{3,4}$", value, "Invalid csc value")


class CardResponseBase(ModelConfigBase):
    """
    Данные карты из ответа ЮKassa.

    Форматы здесь намеренно не проверяются: это данные ЮKassa, а не наши, и строгая
    проверка ответа только превращает любую неожиданность в отказ разобрать платёж.
    """

    first6: str | None = None
    last4: str
    card_type: CardType
    issuer_country: str | None = None
    issuer_name: str | None = None


class CardResponse(CardResponseBase):
    expiry_year: str
    expiry_month: str
    card_product: CardProduct | None = None
    source: CardSource | None = None
