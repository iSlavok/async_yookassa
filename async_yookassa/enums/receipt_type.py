from async_yookassa.enums.base import OpenStrEnum


class ReceiptType(OpenStrEnum):
    payment = "payment"
    refund = "refund"
