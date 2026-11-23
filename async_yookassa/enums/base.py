"""Base class for enums of values that come from YooKassa responses."""

from enum import StrEnum
from typing import Self


class OpenStrEnum(StrEnum):
    """
    Перечисление, которое не падает на незнакомом значении.

    ЮKassa регулярно добавляет новые статусы, причины отмены, способы оплаты и т. п.
    Закрытое перечисление отвергло бы весь ответ (или вебхук) из-за одного нового
    значения. Здесь известные значения остаются обычными членами, а незнакомая
    строка превращается в псевдо-член с тем же значением: он равен исходной
    строке и сериализуется в неё же. Не-строки по-прежнему отвергаются.
    """

    @classmethod
    def _missing_(cls, value: object) -> Self | None:
        if not isinstance(value, str):
            return None
        member = str.__new__(cls, value)
        member._name_ = value
        member._value_ = value
        return member
