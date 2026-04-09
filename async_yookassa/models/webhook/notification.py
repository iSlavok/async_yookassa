from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field

from async_yookassa.enums.webhook_event import WebhookEvent
from async_yookassa.models.deal import DealResponse
from async_yookassa.models.payment import PaymentResponse
from async_yookassa.models.payment_method import PaymentMethodResponse
from async_yookassa.models.payout import PayoutResponse
from async_yookassa.models.refund import RefundResponse


class BaseWebhookNotification(BaseModel):
    type: Literal["notification"] = Field(
        default="notification",
        title="Тип объекта",
        description="Фиксированное значение: `notification`.",
    )


class PaymentWebhookNotification(BaseWebhookNotification):
    """Уведомление о событии платежа."""

    event: Literal[
        WebhookEvent.PAYMENT_WAITING_FOR_CAPTURE,
        WebhookEvent.PAYMENT_SUCCEEDED,
        WebhookEvent.PAYMENT_CANCELED,
    ] = Field(
        title="Тип события",
        description=(
            "Событие, которое вызвало уведомление. Возможные значения:\n\n"
            "- `payment.waiting_for_capture` — платёж подтверждён пользователем и ожидает подтверждения магазином;\n"
            "- `payment.succeeded` — платёж успешно завершён;\n"
            "- `payment.canceled` — платёж отменён."
        ),
    )
    object: PaymentResponse = Field(
        title="Объект платежа",
        description="Полный объект платежа в том состоянии, в котором он находился на момент наступления события.",
    )


class RefundWebhookNotification(BaseWebhookNotification):
    """Уведомление о событии возврата."""

    event: Literal[WebhookEvent.REFUND_SUCCEEDED] = Field(
        title="Тип события",
        description="Событие, которое вызвало уведомление. Значение: `refund.succeeded` — возврат успешно завершён.",
    )
    object: RefundResponse = Field(
        title="Объект возврата",
        description="Полный объект возврата в том состоянии, в котором он находился на момент наступления события.",
    )


class PayoutWebhookNotification(BaseWebhookNotification):
    """Уведомление о событии выплаты."""

    event: Literal[
        WebhookEvent.PAYOUT_SUCCEEDED,
        WebhookEvent.PAYOUT_CANCELED,
    ] = Field(
        title="Тип события",
        description=(
            "Событие, которое вызвало уведомление. Возможные значения:\n\n"
            "- `payout.succeeded` — выплата успешно завершена;\n"
            "- `payout.canceled` — выплата отменена."
        ),
    )
    object: PayoutResponse = Field(
        title="Объект выплаты",
        description="Полный объект выплаты в том состоянии, в котором он находился на момент наступления события.",
    )


class DealWebhookNotification(BaseWebhookNotification):
    """Уведомление о событии сделки."""

    event: Literal[WebhookEvent.DEAL_CLOSED] = Field(
        title="Тип события",
        description="Событие, которое вызвало уведомление. Значение: `deal.closed` — сделка закрыта после успешной выплаты продавцу.",
    )
    object: DealResponse = Field(
        title="Объект сделки",
        description="Полный объект сделки в том состоянии, в котором он находился на момент наступления события.",
    )


class PaymentMethodWebhookNotification(BaseWebhookNotification):
    """Уведомление о сохранении способа оплаты."""

    event: Literal[WebhookEvent.PAYMENT_METHOD_ACTIVE] = Field(
        title="Тип события",
        description="Событие, которое вызвало уведомление. Значение: `payment_method.active` — способ оплаты сохранён и активирован для автоплатежей.",
    )
    object: PaymentMethodResponse = Field(
        title="Объект способа оплаты",
        description="Полный объект сохранённого способа оплаты в том состоянии, в котором он находился на момент наступления события.",
    )


WebhookNotification = Annotated[
    Union[
        PaymentWebhookNotification,
        RefundWebhookNotification,
        PayoutWebhookNotification,
        DealWebhookNotification,
        PaymentMethodWebhookNotification,
    ],
    Field(discriminator="event"),
]
