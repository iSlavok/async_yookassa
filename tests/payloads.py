"""Синтетические ответы ЮKassa в формате из документации."""

from typing import Any

PAYMENT_ID = "2f0c1e3a-000f-5000-9000-1b2c3d4e5f60"


def card(**overrides: Any) -> dict[str, Any]:
    return {
        "first6": "555555",
        "last4": "4444",
        "expiry_year": "2030",
        "expiry_month": "07",
        "card_type": "MasterCard",
        **overrides,
    }


def payment(payment_method: dict[str, Any] | None = None, **overrides: Any) -> dict[str, Any]:
    body: dict[str, Any] = {
        "id": PAYMENT_ID,
        "status": "succeeded",
        "paid": True,
        "amount": {"value": "2249.00", "currency": "RUB"},
        "income_amount": {"value": "2170.29", "currency": "RUB"},
        "authorization_details": {"rrn": "603668680243", "auth_code": "000000", "three_d_secure": {"applied": False}},
        "captured_at": "2026-11-22T16:02:43.820Z",
        "created_at": "2026-11-22T16:01:27.000Z",
        "description": "Подписка",
        "metadata": {},
        "recipient": {"account_id": "100500", "gateway_id": "100700"},
        "refundable": True,
        "refunded_amount": {"value": "0.00", "currency": "RUB"},
        "test": False,
    }
    if payment_method is not None:
        body["payment_method"] = payment_method
    body.update(overrides)
    return body


def payment_method(type_: str, **fields: Any) -> dict[str, Any]:
    return {"type": type_, "id": PAYMENT_ID, "saved": False, "status": "inactive", **fields}


def notification(event: str, obj: dict[str, Any]) -> dict[str, Any]:
    return {"type": "notification", "event": event, "object": obj}


def binding(type_: str, **fields: Any) -> dict[str, Any]:
    return {
        "type": type_,
        "id": "1da5c87d-0984-50e8-a7f3-8de646dd9ec9",
        "saved": True,
        "status": "active",
        "holder": {"account_id": "100500"},
        **fields,
    }


def refund(**overrides: Any) -> dict[str, Any]:
    return {
        "id": "216749f7-0016-50be-b000-078d43a63ae4",
        "payment_id": PAYMENT_ID,
        "status": "succeeded",
        "created_at": "2026-11-22T16:10:00.000Z",
        "amount": {"value": "100.00", "currency": "RUB"},
        **overrides,
    }
