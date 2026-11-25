from async_yookassa.enums.base import OpenStrEnum


class PaymentDetailsStatusEnum(OpenStrEnum):
    pending = "pending"
    waiting_for_capture = "waiting_for_capture"
    succeeded = "succeeded"
    canceled = "canceled"
