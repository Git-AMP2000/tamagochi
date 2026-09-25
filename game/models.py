"""Модели предметов игры."""

from dataclasses import dataclass


@dataclass
class Food:
    """Еда для питомца."""

    name: str
    satiety: int
    price: int

    def __repr__(self) -> str:
        """Возвращает название еды."""
        return self.name


@dataclass
class Medicine:
    """Лекарство для питомца."""

    name: str
    price: int
    heal_hp: int
    number_of_uses: int
    uses: int = 0

    def is_empty(self) -> bool:
        """Проверяет, закончились ли использования лекарства."""
        return self.uses >= self.number_of_uses

    def __repr__(self) -> str:
        """Возвращает название лекарства."""
        return self.name
