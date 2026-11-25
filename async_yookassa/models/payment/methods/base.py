from datetime import datetime
from typing import Annotated, Literal, Union

from pydantic import BaseModel, ConfigDict, Field, Tag

from async_yookassa.enums.payment import PaymentMethodStatus, PaymentMethodType
from async_yookassa.models.base import ModelConfigBase
from async_yookassa.models.discriminator import UNKNOWN_TAG, open_discriminator
from async_yookassa.models.payment.amount import Amount
from async_yookassa.models.payment.methods.articles import (
    ArticleRefund,
    ArticleResponse,
)
from async_yookassa.models.payment.methods.card import (
    CardResponse,
)
from async_yookassa.models.payment.methods.electronic_certificate import (
    ElectronicCertificate,
)
from async_yookassa.models.payment.methods.payer_bank_details import (
    B2BSBPayerBankDetails,
    SBPPayerBankDetails,
)
from async_yookassa.models.payment.methods.vat_data import (
    VatDataUnion,
)


class PaymentMethodBase(BaseModel):
    id: str
    saved: bool
    status: PaymentMethodStatus
    title: str | None = None

    model_config = ConfigDict(use_enum_values=True)


class SberLoanPaymentMethod(PaymentMethodBase):
    type: Literal[PaymentMethodType.sber_loan]
    discount_amount: Amount | None = None
    # `loan` или `installments_N` на сегодня; по спецификации — просто строка.
    loan_option: str | None = None
    suspended_until: datetime | None = None


class AlfabankPaymentMethod(PaymentMethodBase):
    type: Literal[PaymentMethodType.alfabank]
    login: str | None = None


class GenericPaymentMethod(PaymentMethodBase):
    type: Literal[
        PaymentMethodType.mobile_balance,
        PaymentMethodType.installments,
        PaymentMethodType.cash,
        PaymentMethodType.sber_bnpl,
        PaymentMethodType.apple_pay,
        PaymentMethodType.google_pay,
        PaymentMethodType.qiwi,
        PaymentMethodType.wechat,
        PaymentMethodType.webmoney,
    ]


class BankCardPaymentMethod(PaymentMethodBase):
    type: Literal[PaymentMethodType.bank_card]
    card: CardResponse | None = None


class AlfaPayPaymentMethod(PaymentMethodBase):
    type: Literal[PaymentMethodType.alfa_pay]
    card: CardResponse | None = None


class SBPPaymentMethodBase(PaymentMethodBase):
    type: Literal[PaymentMethodType.sbp]
    sbp_operation_id: str | None = None


class SBPPaymentMethodResponse(SBPPaymentMethodBase):
    payer_bank_details: SBPPayerBankDetails | None = None


class B2BSberbankPaymentMethod(PaymentMethodBase):
    type: Literal[PaymentMethodType.b2b_sberbank]
    payer_bank_details: B2BSBPayerBankDetails | None = None
    payment_purpose: str = Field(max_length=210)
    vat_data: VatDataUnion


class ElectronicCertificatePaymentMethodBase(BankCardPaymentMethod):
    type: Literal[PaymentMethodType.electronic_certificate]
    electronic_certificate: ElectronicCertificate | None = None


class ElectronicCertificatePaymentMethodResponse(ElectronicCertificatePaymentMethodBase):
    articles: list[ArticleResponse] | None = None


class ElectronicCertificatePaymentMethodRefund(ModelConfigBase):
    """Возврат на электронный сертификат: и в запросе возврата, и в ответе."""

    type: Literal[PaymentMethodType.electronic_certificate]
    electronic_certificate: ElectronicCertificate | None = None
    articles: list[ArticleRefund] | None = None


class YooMoneyPaymentMethod(PaymentMethodBase):
    type: Literal[PaymentMethodType.yoo_money]
    account_number: str | None = None


class SberPayPaymentMethod(BankCardPaymentMethod):
    type: Literal[PaymentMethodType.sberbank]
    phone: str | None = None


class TPayPaymentMethod(BankCardPaymentMethod):
    type: Literal[PaymentMethodType.tinkoff_bank]


class UnknownPaymentMethod(BaseModel):
    """
    Способ оплаты, которого эта версия библиотеки ещё не знает.

    Нужен, чтобы новый способ оплаты в ЮKassa не ломал разбор всего платежа.
    Все поля ответа сохраняются: известные базовые — как атрибуты, остальные — в ``model_extra``.
    """

    type: str
    id: str | None = None
    saved: bool | None = None
    status: PaymentMethodStatus | None = None
    title: str | None = None

    model_config = ConfigDict(extra="allow", use_enum_values=True)


_PAYMENT_METHODS = (
    SberLoanPaymentMethod,
    AlfabankPaymentMethod,
    AlfaPayPaymentMethod,
    BankCardPaymentMethod,
    SBPPaymentMethodResponse,
    B2BSberbankPaymentMethod,
    ElectronicCertificatePaymentMethodResponse,
    YooMoneyPaymentMethod,
    SberPayPaymentMethod,
    TPayPaymentMethod,
    GenericPaymentMethod,
)

PaymentMethodUnion = Annotated[
    Union[
        Annotated[SberLoanPaymentMethod, Tag("SberLoanPaymentMethod")],
        Annotated[AlfabankPaymentMethod, Tag("AlfabankPaymentMethod")],
        Annotated[AlfaPayPaymentMethod, Tag("AlfaPayPaymentMethod")],
        Annotated[BankCardPaymentMethod, Tag("BankCardPaymentMethod")],
        Annotated[SBPPaymentMethodResponse, Tag("SBPPaymentMethodResponse")],
        Annotated[B2BSberbankPaymentMethod, Tag("B2BSberbankPaymentMethod")],
        Annotated[ElectronicCertificatePaymentMethodResponse, Tag("ElectronicCertificatePaymentMethodResponse")],
        Annotated[YooMoneyPaymentMethod, Tag("YooMoneyPaymentMethod")],
        Annotated[SberPayPaymentMethod, Tag("SberPayPaymentMethod")],
        Annotated[TPayPaymentMethod, Tag("TPayPaymentMethod")],
        Annotated[GenericPaymentMethod, Tag("GenericPaymentMethod")],
        Annotated[UnknownPaymentMethod, Tag(UNKNOWN_TAG)],
    ],
    open_discriminator("type", *_PAYMENT_METHODS),
]


class SBPRefundMethod(BaseModel):
    type: Literal[PaymentMethodType.sbp]
    sbp_operation_id: str | None = None

    model_config = ConfigDict(use_enum_values=True)


class UnknownRefundMethod(BaseModel):
    """Способ возврата, которого эта версия библиотеки ещё не знает."""

    type: str

    model_config = ConfigDict(extra="allow")


PaymentMethodRefundUnion = Annotated[
    Union[
        Annotated[SBPRefundMethod, Tag("SBPRefundMethod")],
        Annotated[ElectronicCertificatePaymentMethodRefund, Tag("ElectronicCertificatePaymentMethodRefund")],
        Annotated[UnknownRefundMethod, Tag(UNKNOWN_TAG)],
    ],
    open_discriminator("type", SBPRefundMethod, ElectronicCertificatePaymentMethodRefund),
]
