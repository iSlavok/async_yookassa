"""Сервисы: ответ, который не разобрался, не должен теряться."""

import asyncio
from typing import Any

import pytest

from async_yookassa.exceptions import APIError, ResponseParsingError
from async_yookassa.models.payment import PaymentResponse
from async_yookassa.services.payment import PaymentService
from tests.payloads import PAYMENT_ID, payment


class FakeHttp:
    def __init__(self, response: dict[str, Any]) -> None:
        self.response = response

    async def request(self, **_kwargs: Any) -> dict[str, Any]:
        return self.response


def test_find_one_parses_the_response():
    service = PaymentService(FakeHttp(payment()))  # type: ignore[arg-type]

    parsed = asyncio.run(service.find_one(PAYMENT_ID))

    assert isinstance(parsed, PaymentResponse)


def test_unparsable_response_is_an_api_error_with_the_raw_body():
    """Деньги уже могли списаться: вызывающему нужен хотя бы id платежа из ответа."""
    raw = {"id": PAYMENT_ID, "status": "succeeded"}
    service = PaymentService(FakeHttp(raw))  # type: ignore[arg-type]

    with pytest.raises(APIError) as caught:
        asyncio.run(service.find_one(PAYMENT_ID))

    assert isinstance(caught.value, ResponseParsingError)
    assert caught.value.raw["id"] == PAYMENT_ID
    assert caught.value.model is PaymentResponse
