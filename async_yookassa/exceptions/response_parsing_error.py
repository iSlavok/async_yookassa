from typing import Any

from async_yookassa.exceptions.api_error import APIError


class ResponseParsingError(APIError):
    """
    ЮKassa ответила успешно, но ответ не удалось разобрать в модель.

    Запрос при этом уже выполнен: платёж мог быть создан, а деньги — списаны.
    Поэтому исходный ответ сохраняется в ``raw`` — из него можно достать хотя бы ``id``.
    """

    def __init__(self, model: type, raw: dict[str, Any], errors: str) -> None:
        super().__init__(f"Failed to parse YooKassa response as {model.__name__}: {errors}")
        self.model = model
        self.raw = raw
