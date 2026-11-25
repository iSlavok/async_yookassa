"""
Сверка перечислений библиотеки с официальной OpenAPI-спецификацией ЮKassa.

Спецификация лежит в ``tests/data/yookassa-openapi.json`` (скачана с
https://yookassa.ru/developers/api/yookassa-openapi-specification.yaml и сконвертирована в JSON).
Обновил файл — тест покажет, каких новых значений библиотека ещё не знает, до того как их пришлёт прод.
Благодаря открытым перечислениям новые значения прод не уронят, но знать о них стоит.
"""

import json
from enum import Enum
from pathlib import Path

import pytest

from async_yookassa.enums import payment as payment_enums
from async_yookassa.enums.agent_type import AgentTypeEnum
from async_yookassa.enums.deal_enums import DealFeeMomentEnum, DealStatusEnum
from async_yookassa.enums.fiscalization import FiscalizationProviderEnum
from async_yookassa.enums.item_measure import ItemMeasureEnum
from async_yookassa.enums.payment_methods import PaymentMethodType as BindingType
from async_yookassa.enums.payment_subject import PaymentModeEnum, PaymentSubjectEnum
from async_yookassa.enums.payout import PayoutTypeEnum
from async_yookassa.enums.personal_data_enums import PersonalDataTypeEnum
from async_yookassa.enums.receipt_type import ReceiptType
from async_yookassa.enums.receiver import ReceiverTypeEnum
from async_yookassa.enums.status import OperationStatus
from async_yookassa.enums.transfers import TransferStatusEnum
from async_yookassa.enums.vat_data import VatDataTypeEnum
from async_yookassa.models.payment.methods.base import _PAYMENT_METHODS

SCHEMAS = json.loads((Path(__file__).parent / "data" / "yookassa-openapi.json").read_text())["components"]["schemas"]

ENUMS: dict[str, type[Enum]] = {
    "PaymentMethodType": payment_enums.PaymentMethodType,
    "PaymentStatus": payment_enums.PaymentStatus,
    "ReceiptRegistrationStatus": payment_enums.ReceiptRegistrationStatus,
    "PaymentMethodStatus": payment_enums.PaymentMethodStatus,
    "ConfirmationType": payment_enums.ConfirmationType,
    "BankCardType": payment_enums.CardType,
    "BankCardDataSource": payment_enums.CardSource,
    "SavePaymentMethodType": BindingType,
    "FiscalizationProvider": FiscalizationProviderEnum,
    "ReceiptItemMeasure": ItemMeasureEnum,
    "ReceiptItemPaymentSubject": PaymentSubjectEnum,
    "ReceiptItemPaymentMode": PaymentModeEnum,
    "ReceiptItemAgentType": AgentTypeEnum,
    "ReceiptType": ReceiptType,
    "ReceiverType": ReceiverTypeEnum,
    "TransferStatus": TransferStatusEnum,
    "B2bSberbankVatDataType": VatDataTypeEnum,
    "RefundStatus": OperationStatus,
    "PayoutStatus": OperationStatus,
    "InvoiceStatus": OperationStatus,
    "DealStatus": DealStatusEnum,
    "FeeMoment": DealFeeMomentEnum,
    "PayoutDestinationType": PayoutTypeEnum,
    "PersonalDataType": PersonalDataTypeEnum,
}


@pytest.mark.parametrize(("schema", "enum"), ENUMS.items(), ids=ENUMS.keys())
def test_library_knows_every_documented_value(schema, enum):
    documented = set(SCHEMAS[schema]["enum"])
    known = {member.value for member in enum}

    assert documented <= known, f"{enum.__name__} is missing {sorted(documented - known)}"


def test_every_documented_payment_method_has_a_model():
    documented = set(SCHEMAS["PaymentMethod"]["discriminator"]["mapping"])
    modelled = {str(value) for model in _PAYMENT_METHODS for value in model.model_fields["type"].annotation.__args__}

    assert documented <= modelled, f"no model for {sorted(documented - modelled)}"
