from async_yookassa.enums.base import OpenStrEnum


class AgentTypeEnum(OpenStrEnum):
    banking_payment_agent = "banking_payment_agent"
    banking_payment_subagent = "banking_payment_subagent"
    payment_agent = "payment_agent"
    payment_subagent = "payment_subagent"
    attorney = "attorney"
    commissioner = "commissioner"
    agent = "agent"
