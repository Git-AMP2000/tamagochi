"""Логика кликера."""

from __future__ import annotations

import random
from abc import ABC, abstractmethod


class AbstractClicker(ABC):
    """Интерфейс кликера."""

    def __init__(self) -> None:
        """Инициализирует кликер."""

    @abstractmethod
    def click(self) -> None:
        """Выполняет один клик."""

    @abstractmethod
    def income_per_click(self) -> int:
        """Возвращает доход за последний клик."""


class Clicker(AbstractClicker):
    """Кликер со случайным доходом."""

    def __init__(self, min_income: int = 10, max_income: int = 20) -> None:
        """Создаёт кликер с диапазоном дохода."""
        if min_income < 0:
            raise ValueError("Минимальный доход не может быть отрицательным.")
        if max_income < min_income:
            raise ValueError(
                "Максимальный доход не может быть меньше минимального."
            )
        self._min_income = min_income
        self._max_income = max_income
        self._income_per_click = 0

    def click(self) -> None:
        """Совершает клик и обновляет доход."""
        self._income_per_click = random.randint(
            self._min_income, self._max_income
        )

    def income_per_click(self) -> int:
        """Возвращает доход за последний клик."""
        return self._income_per_click


# Совместимость со старым именем
SimpleRandomClicker = Clicker
