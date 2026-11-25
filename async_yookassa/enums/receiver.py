from async_yookassa.enums.base import OpenStrEnum


class ReceiverTypeEnum(OpenStrEnum):
    bank_account = "bank_account"
    mobile_balance = "mobile_balance"
    digital_wallet = "digital_wallet"
