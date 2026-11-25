from async_yookassa.enums.base import OpenStrEnum


class InvoicePartyEnum(OpenStrEnum):
    yoo_money = "yoo_money"
    merchant = "merchant"


class InvoiceReasonEnum(OpenStrEnum):
    invoice_canceled = "invoice_canceled"
    invoice_expired = "invoice_expired"
    general_decline = "general_decline"
    payment_canceled = "payment_canceled"
    payment_expired_on_capture = "payment_expired_on_capture"
