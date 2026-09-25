"""Логика питомца."""

from __future__ import annotations

from abc import ABC, abstractmethod

from .exceptions import MedicineEmptyError, TamagochiDeadError
from .models import Food, Medicine


class AbstractTamagochi(ABC):
    """Интерфейс питомца."""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """Накормить питомца."""

    @abstractmethod
    def play(self) -> None:
        """Поиграть с питомцем."""

    @abstractmethod
    def rest(self) -> None:
        """Дать питомцу отдохнуть."""

    @abstractmethod
    def heal(self, medicine: Medicine) -> None:
        """Вылечить питомца."""

    @abstractmethod
    def status(self) -> dict[str, int]:
        """Получить данные обо всех показателях питомца."""

    @abstractmethod
    def is_alive(self) -> bool:
        """Проверить, жив ли питомец."""

    @abstractmethod
    def is_sick(self) -> bool:
        """Проверить, болен ли питомец."""

    @abstractmethod
    def update(self) -> None:
        """Обновить состояние питомца за один тик."""


class SimpleTamagochi(AbstractTamagochi):
    """Простая реализация питомца."""

    MAX_STAT = 100

    def __init__(self) -> None:
        """Создаёт питомца с начальными показателями."""
        self._hunger = 30
        self._fatigue = 20
        self._hp = 100
        self._energy = 80
        self._sick = False

    def _ensure_alive(self) -> None:
        """Проверяет, жив ли питомец."""
        if not self.is_alive():
            raise TamagochiDeadError("Питомец мёртв.")

    def feed(self, food: Food) -> None:
        """Кормит питомца, уменьшая голод."""
        self._ensure_alive()
        self._hunger = max(0, self._hunger - food.satiety)
        self._energy = max(0, self._energy - 5)
        self._fatigue = min(self.MAX_STAT, self._fatigue + 2)

    def play(self) -> None:
        """Играет с питомцем."""
        self._ensure_alive()
        self._energy = max(0, self._energy - 15)
        self._hunger = min(self.MAX_STAT, self._hunger + 10)
        self._fatigue = min(self.MAX_STAT, self._fatigue + 10)

    def rest(self) -> None:
        """Даёт питомцу отдохнуть."""
        self._ensure_alive()
        energy_gain = 10 if self._sick else 25
        self._energy = min(self.MAX_STAT, self._energy + energy_gain)
        self._fatigue = max(0, self._fatigue - 20)
        self._hunger = min(self.MAX_STAT, self._hunger + 5)

    def heal(self, medicine: Medicine) -> None:
        """Лечит питомца лекарством."""
        self._ensure_alive()
        if medicine.is_empty():
            raise MedicineEmptyError("Лекарство закончилось.")
        self._hp = min(self.MAX_STAT, self._hp + medicine.heal_hp)
        medicine.uses += 1
        if self._hp > 30:
            self._sick = False

    def status(self) -> dict[str, int]:
        """Возвращает текущие показатели питомца."""
        return {
            "hunger": self._hunger,
            "fatigue": self._fatigue,
            "hp": self._hp,
            "energy": self._energy,
        }

    def is_alive(self) -> bool:
        """Проверяет, жив ли питомец."""
        return self._hp > 0

    def is_sick(self) -> bool:
        """Проверяет, болен ли питомец."""
        return self._sick

    def update(self) -> None:
        """Обновляет состояние питомца за один тик."""
        if not self.is_alive():
            return

        self._hunger = min(self.MAX_STAT, self._hunger + 5)
        self._fatigue = min(self.MAX_STAT, self._fatigue + 5)
        self._energy = max(0, self._energy - 5)

        if self._sick:
            self._hp -= 5
            self._fatigue = min(self.MAX_STAT, self._fatigue + 5)

        if self._hunger > 80:
            self._hp -= 5
        if self._fatigue > 80:
            self._hp -= 5

        if self._hp <= 20 and not self._sick:
            self._sick = True
