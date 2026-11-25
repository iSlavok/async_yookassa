from async_yookassa.enums.base import OpenStrEnum


class PersonalDataTypeEnum(OpenStrEnum):
    sbp_payout_recipient = "sbp_payout_recipient"
    payout_statement_recipient = "payout_statement_recipient"


class PersonalDataStatusEnum(OpenStrEnum):
    waiting_for_operation = "waiting_for_operation"
    active = "active"
    canceled = "canceled"
