from async_yookassa.enums.base import OpenStrEnum


class OperationStatus(OpenStrEnum):
    """Статус возврата, выплаты, чека или счёта."""

    pending = "pending"
    succeeded = "succeeded"
    canceled = "canceled"
