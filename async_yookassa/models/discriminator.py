"""Discriminated unions that survive values this library doesn't know yet."""

from collections.abc import Callable
from typing import Any, Literal, get_args, get_origin

from pydantic import BaseModel, Discriminator

UNKNOWN_TAG = "unknown"


def open_discriminator(field: str, *variants: type[BaseModel]) -> Discriminator:
    """
    Дискриминатор union'а, который не падает на незнакомом значении поля.

    Обычный ``Field(discriminator=...)`` отвергает весь объект, если ЮKassa прислала
    значение, которого нет в union'е (новый способ оплаты, новое событие вебхука).
    Здесь значение ищется среди ``Literal``-аннотаций поля ``field`` у вариантов,
    а всё незнакомое уходит в вариант с тегом ``UNKNOWN_TAG``.

    Каждый вариант union'а помечается ``Tag(<имя класса>)``, запасной — ``Tag(UNKNOWN_TAG)``.
    """
    tags: dict[str, str] = {}
    for variant in variants:
        annotation = variant.model_fields[field].annotation
        if get_origin(annotation) is not Literal:
            msg = f"{variant.__name__}.{field} must be annotated with Literal"
            raise TypeError(msg)
        for value in get_args(annotation):
            tags[str(value)] = variant.__name__
    return Discriminator(_resolver(field, tags))


def _resolver(field: str, tags: dict[str, str]) -> Callable[[Any], str]:
    def resolve(data: Any) -> str:
        value = data.get(field) if isinstance(data, dict) else getattr(data, field, None)
        if value is None:
            return UNKNOWN_TAG
        return tags.get(str(value), UNKNOWN_TAG)

    return resolve
