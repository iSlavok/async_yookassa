from async_yookassa.enums.base import OpenStrEnum


class PayoutTypeEnum(OpenStrEnum):
    bank_card = "bank_card"
    sbp = "sbp"
    yoo_money = "yoo_money"
