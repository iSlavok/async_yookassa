"""Разбор входящих уведомлений: ЮKassa повторяет не-200 сутки, а потом событие теряется."""

from pydantic import TypeAdapter

from async_yookassa.models.payment.methods.base import AlfaPayPaymentMethod, UnknownPaymentMethod
from async_yookassa.models.webhook.notification import (
    PaymentMethodWebhookNotification,
    PaymentWebhookNotification,
    UnknownWebhookNotification,
    WebhookNotification,
)
from tests.payloads import binding, card, notification, payment, payment_method

ADAPTER = TypeAdapter(WebhookNotification)


def test_payment_succeeded_paid_with_alfa_pay():
    parsed = ADAPTER.validate_python(
        notification("payment.succeeded", payment(payment_method("alfa_pay", card=card())))
    )

    assert isinstance(parsed, PaymentWebhookNotification)
    assert isinstance(parsed.object.payment_method, AlfaPayPaymentMethod)


def test_payment_succeeded_with_unknown_payment_method():
    raw = notification("payment.succeeded", payment(payment_method("yet_unknown_pay")))

    parsed = ADAPTER.validate_python(raw)

    assert isinstance(parsed, PaymentWebhookNotification)
    assert parsed.object.id == raw["object"]["id"]
    assert isinstance(parsed.object.payment_method, UnknownPaymentMethod)


def test_unknown_event_keeps_raw_object():
    raw = notification("refund.canceled", {"id": "r-1", "status": "canceled"})

    parsed = ADAPTER.validate_python(raw)

    assert isinstance(parsed, UnknownWebhookNotification)
    assert parsed.event == "refund.canceled"
    assert parsed.object == {"id": "r-1", "status": "canceled"}


def test_unknown_event_from_json():
    parsed = ADAPTER.validate_json('{"type": "notification", "event": "invoice.paid", "object": {"id": "i"}}')

    assert isinstance(parsed, UnknownWebhookNotification)


def test_sbp_binding_activated():
    """Привязка через СБП есть в документации с июня 2026."""
    raw = notification("payment_method.active", binding("sbp", payer_bank_details={"bank_id": "100000000111"}))

    parsed = ADAPTER.validate_python(raw)

    assert isinstance(parsed, PaymentMethodWebhookNotification)
    assert parsed.object.type == "sbp"
    assert parsed.object.payer_bank_details is not None
    assert parsed.object.payer_bank_details.bank_id == "100000000111"
