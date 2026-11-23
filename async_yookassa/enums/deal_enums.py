from async_yookassa.enums.base import OpenStrEnum


class DealTypeEnum(OpenStrEnum):
    safe_deal = "safe_deal"


class DealFeeMomentEnum(OpenStrEnum):
    payment_succeeded = "payment_succeeded"
    deal_closed = "deal_closed"


class DealStatusEnum(OpenStrEnum):
    opened = "opened"
    closed = "closed"
