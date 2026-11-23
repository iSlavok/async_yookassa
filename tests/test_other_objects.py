"""Привязка, возврат, выплата, чек, счёт, магазин, перс. данные — места, где разбор падал."""

import pytest
from pydantic import ValidationError

from async_yookassa.models.me.response import MeResponse
from async_yookassa.models.payment.methods.base import (
    ElectronicCertificatePaymentMethodRefund,
    UnknownRefundMethod,
)
from async_yookassa.models.payment.methods.card import CardRequest
from async_yookassa.models.payment.receipts.receipt_item import ReceiptItem
from async_yookassa.models.payment_method import PaymentMethodRequest, PaymentMethodResponse
from async_yookassa.models.payment_method.confirmation import QRConfirmationResponse
from async_yookassa.models.payout.payout_destination import UnknownPayoutDestination
from async_yookassa.models.payout.response import PayoutResponse
from async_yookassa.models.personal_data.response import PersonalDataResponse
from async_yookassa.models.receipt.response import ReceiptResponse
from async_yookassa.models.refund.request import RefundRequest
from async_yookassa.models.refund.response import RefundResponse
from tests.payloads import PAYMENT_ID, binding, refund

E_CERT = {
    "type": "electronic_certificate",
    "electronic_certificate": {"amount": {"value": "100.00", "currency": "RUB"}, "basket_id": "b-1"},
}


def test_binding_with_qr_confirmation_and_metadata():
    raw = binding(
        "sbp",
        status="pending",
        confirmation={"type": "qr", "confirmation_data": "https://qr.nspk.ru/x"},
        metadata={"user": "1"},
    )

    parsed = PaymentMethodResponse.model_validate(raw)

    assert isinstance(parsed.confirmation, QRConfirmationResponse)
    assert parsed.metadata == {"user": "1"}


def test_binding_request_accepts_sbp_with_qr():
    request = PaymentMethodRequest.model_validate({"type": "sbp", "confirmation": {"type": "qr"}, "metadata": {"a": 1}})

    assert request.model_dump(exclude_none=True) == {
        "type": "sbp",
        "confirmation": {"type": "qr"},
        "metadata": {"a": 1},
    }


@pytest.mark.parametrize(
    ("party", "reason"), [("refund_network", "payment_expired"), ("future_party", "future_reason")]
)
def test_refund_cancellation_details(party, reason):
    parsed = RefundResponse.model_validate(
        refund(status="canceled", cancellation_details={"party": party, "reason": reason}),
    )

    assert parsed.cancellation_details.party == party


def test_refund_to_electronic_certificate():
    """Раньше модель требовала id/saved/status сохранённого способа оплаты, которых у возврата нет."""
    parsed = RefundResponse.model_validate(refund(refund_method=E_CERT))

    assert isinstance(parsed.refund_method, ElectronicCertificatePaymentMethodRefund)


def test_refund_request_to_electronic_certificate():
    request = RefundRequest(
        payment_id=PAYMENT_ID, amount={"value": "100.00", "currency": "RUB"}, refund_method_data=E_CERT
    )

    assert request.refund_method_data is not None


def test_refund_with_unknown_status_and_method():
    parsed = RefundResponse.model_validate(refund(status="new_status", refund_method={"type": "new_method", "x": 1}))

    assert parsed.status == "new_status"
    assert isinstance(parsed.refund_method, UnknownRefundMethod)


def test_payout_cancellation_and_unknown_destination():
    parsed = PayoutResponse.model_validate(
        {
            "id": "po-28559c7f-000f-5000-a000-1e8e5a5c3e5c",
            "amount": {"value": "10.00", "currency": "RUB"},
            "status": "canceled",
            "payout_destination": {"type": "new_destination"},
            "created_at": "2026-11-22T16:10:00.000Z",
            "test": False,
            "cancellation_details": {"party": "payout_network", "reason": "self_employed_annual_limit_exceeded"},
        },
    )

    assert isinstance(parsed.payout_destination, UnknownPayoutDestination)
    assert parsed.cancellation_details.reason == "self_employed_annual_limit_exceeded"


def test_receipt_without_tax_system_code_and_timezone():
    parsed = ReceiptResponse.model_validate(
        {"id": "rt-2da5c87d-0384-50e8-a7f3-8d5646dd9e10", "type": "payment", "status": "succeeded", "items": []},
    )

    assert parsed.tax_system_code is None
    assert parsed.timezone is None


def test_me_with_new_provider_and_payment_method():
    parsed = MeResponse.model_validate(
        {
            "account_id": "100500",
            "status": "enabled",
            "test": False,
            "fiscalization": {"enabled": True, "provider": "yoo_receipt"},
            "payment_methods": ["bank_card", "alfa_pay", "future_pay"],
        },
    )

    assert parsed.payment_methods == ["bank_card", "alfa_pay", "future_pay"]


def test_personal_data_expired_by_timeout():
    parsed = PersonalDataResponse.model_validate(
        {
            "id": "pd-2da5c87d-0384-50e8-a7f3-8d5646dd9e10",
            "type": "sbp_payout_recipient",
            "status": "canceled",
            "created_at": "2026-11-22T16:10:00.000Z",
            "cancellation_details": {"party": "yoo_money", "reason": "expired_by_timeout"},
        },
    )

    assert parsed.cancellation_details.reason == "expired_by_timeout"


@pytest.mark.parametrize("field", ["number", "expiry_year", "expiry_month"])
def test_card_request_rejects_non_string_with_validation_error(field):
    """Раньше валидаторы бросали TypeError мимо pydantic — в FastAPI это 500, а не 422."""
    data = {"number": "5555555555554444", "expiry_year": "2030", "expiry_month": "07", field: None}

    with pytest.raises(ValidationError):
        CardRequest.model_validate(data)


def test_card_request_rejects_month_13():
    with pytest.raises(ValidationError):
        CardRequest.model_validate({"number": "5555555555554444", "expiry_year": "2030", "expiry_month": "13"})


def test_receipt_item_mark_mode():
    base = {
        "description": "Подписка",
        "amount": {"value": "1.00", "currency": "RUB"},
        "vat_code": 1,
        "quantity": "1",
    }

    assert ReceiptItem.model_validate({**base, "mark_mode": None}).mark_mode is None
    with pytest.raises(ValidationError):
        ReceiptItem.model_validate({**base, "mark_mode": 5})
