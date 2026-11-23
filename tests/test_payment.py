"""Разбор платежа: способ оплаты, перечисления, необязательные поля."""

import pytest
from pydantic import ValidationError

from async_yookassa.models.payment import PaymentResponse
from async_yookassa.models.payment.methods.base import (
    AlfaPayPaymentMethod,
    BankCardPaymentMethod,
    SberLoanPaymentMethod,
    UnknownPaymentMethod,
)
from tests.payloads import card, payment, payment_method


def test_alfa_pay_is_parsed_with_its_card():
    """Ровно такой платёж вебхук отверг с 422: способа `alfa_pay` не было в union'е."""
    parsed = PaymentResponse.model_validate(payment(payment_method("alfa_pay", card=card())))

    assert isinstance(parsed.payment_method, AlfaPayPaymentMethod)
    assert parsed.payment_method.card is not None
    assert parsed.payment_method.card.last4 == "4444"


def test_unknown_payment_method_keeps_every_field():
    """Следующий новый способ оплаты не должен ломать разбор всего платежа."""
    method = payment_method("yet_unknown_pay", wallet={"id": "w-1"})

    parsed = PaymentResponse.model_validate(payment(method))

    assert isinstance(parsed.payment_method, UnknownPaymentMethod)
    assert parsed.payment_method.type == "yet_unknown_pay"
    assert parsed.payment_method.saved is False
    assert parsed.payment_method.model_extra == {"wallet": {"id": "w-1"}}


def test_unknown_payment_method_survives_json_input():
    parsed = PaymentResponse.model_validate_json(
        '{"id": "x", "status": "succeeded", "paid": true, "refundable": false, "test": false,'
        ' "amount": {"value": "1.00", "currency": "RUB"}, "created_at": "2026-11-22T16:01:27Z",'
        ' "payment_method": {"type": "yet_unknown_pay", "id": "m", "saved": false, "status": "inactive"}}'
    )

    assert isinstance(parsed.payment_method, UnknownPaymentMethod)


def test_known_payment_method_still_validates_strictly():
    """Запасная модель — только для незнакомого типа: известный тип с битыми данными должен падать."""
    with pytest.raises(ValidationError):
        PaymentResponse.model_validate(payment(payment_method("bank_card", card={"last4": "4444"})))


def test_bank_card_is_parsed_as_before():
    parsed = PaymentResponse.model_validate(payment(payment_method("bank_card", card=card())))

    assert isinstance(parsed.payment_method, BankCardPaymentMethod)


def test_unknown_values_in_enums_do_not_fail_the_payment():
    body = payment(
        payment_method("bank_card", card=card(card_type="NewBrand", source="new_wallet")),
        status="some_new_status",
        receipt_registration="some_new_state",
        cancellation_details={"party": "new_party", "reason": "new_reason"},
    )

    parsed = PaymentResponse.model_validate(body)

    assert parsed.status == "some_new_status"
    assert parsed.cancellation_details is not None
    assert parsed.cancellation_details.reason == "new_reason"
    assert isinstance(parsed.payment_method, BankCardPaymentMethod)
    assert parsed.payment_method.card is not None
    assert parsed.payment_method.card.card_type == "NewBrand"


@pytest.mark.parametrize("reason", ["loan_declined", "loan_declined_by_payer", "loan_application_expired"])
def test_documented_loan_cancellation_reasons(reason):
    body = payment(status="canceled", paid=False, cancellation_details={"party": "yoo_money", "reason": reason})

    assert PaymentResponse.model_validate(body).cancellation_details.reason == reason


def test_sber_loan_option_is_any_string():
    """По спецификации `loan_option` — просто строка; раньше всё кроме loan/installments_N падало."""
    parsed = PaymentResponse.model_validate(payment(payment_method("sber_loan", loan_option="new_option")))

    assert isinstance(parsed.payment_method, SberLoanPaymentMethod)
    assert parsed.payment_method.loan_option == "new_option"


def test_recipient_and_three_d_secure_may_be_absent():
    """В примерах вебхуков из документации `recipient` нет."""
    body = payment()
    del body["recipient"]
    body["authorization_details"] = {"rrn": "1"}

    parsed = PaymentResponse.model_validate(body)

    assert parsed.recipient is None


def test_unknown_confirmation_type_is_kept():
    body = payment(status="pending", paid=False, confirmation={"type": "new_flow", "url": "https://example.com"})

    parsed = PaymentResponse.model_validate(body)

    assert parsed.confirmation is not None
    assert parsed.confirmation.type == "new_flow"
