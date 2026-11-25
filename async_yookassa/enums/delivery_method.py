from async_yookassa.enums.base import OpenStrEnum


class DeliveryMethodType(OpenStrEnum):
    SELF = "self"
    SMS = "sms"
    EMAIL = "email"
