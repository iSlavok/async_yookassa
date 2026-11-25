from async_yookassa.enums.base import OpenStrEnum


class VatDataTypeEnum(OpenStrEnum):
    untaxed = "untaxed"
    calculated = "calculated"
    mixed = "mixed"


class RateEnum(OpenStrEnum):
    five = "5"
    seven = "7"
    ten = "10"
    twenty = "20"
    twenty_two = "22"
