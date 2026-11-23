from async_yookassa.enums.base import OpenStrEnum


class MeStatusEnum(OpenStrEnum):
    enabled = "enabled"
    disabled = "disabled"


class PayoutMethodsEnum(OpenStrEnum):
    bank_card = "bank_card"
    yoo_money = "yoo_money"
    sbp = "sbp"
