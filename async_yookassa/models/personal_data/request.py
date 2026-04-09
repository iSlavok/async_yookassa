from datetime import datetime
from typing import Any, Literal

from async_yookassa.enums.personal_data_enums import PersonalDataTypeEnum
from async_yookassa.models.base import ModelConfigBase


class SBPPersonalDataRequest(ModelConfigBase):
    type: Literal[PersonalDataTypeEnum.sbp_payout_recipient] = PersonalDataTypeEnum.sbp_payout_recipient
    last_name: str
    first_name: str
    middle_name: str | None = None
    metadata: dict[str, Any] | None = None


class PayoutStatementRecipientPersonalDataRequest(ModelConfigBase):
    type: Literal[PersonalDataTypeEnum.payout_statement_recipient] = PersonalDataTypeEnum.payout_statement_recipient
    last_name: str
    first_name: str
    middle_name: str | None = None
    metadata: dict[str, Any] | None = None
    birthdate: datetime | None = None
