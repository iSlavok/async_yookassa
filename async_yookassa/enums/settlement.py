from async_yookassa.enums.base import OpenStrEnum


class SettlementTypeEnum(OpenStrEnum):
    payout = "payout"


class SettlementReceiptEnum(OpenStrEnum):
    cashless = "cashless"
    prepayment = "prepayment"
    postpayment = "postpayment"
    consideration = "consideration"
