"""Логика игры."""

from __future__ import annotations

import copy
from abc import ABC, abstractmethod

from .clicker import AbstractClicker
from .exceptions import MedicineEmptyError, TamagochiDeadError
from .models import Food, Medicine
from .tamagochi import AbstractTamagochi


class AbstractGame(ABC):
    """Интерфейс игры."""

    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine],
    ) -> None:
        """Инициализирует игру."""

    @abstractmethod
    def work(self) -> int:
        """Заработать монеты."""

    @abstractmethod
    def buy_food(self) -> None:
        """Купить еду."""

    @abstractmethod
    def buy_medicine(self) -> None:
        """Купить лекарство."""

    @abstractmethod
    def feed_tamagochi(self) -> None:
        """Покормить питомца."""

    @abstractmethod
    def heal_tamagochi(self) -> None:
        """Вылечить питомца."""

    @abstractmethod
    def rest_tamagochi(self) -> None:
        """Уложить питомца отдыхать."""

    @abstractmethod
    def play_with_tamagochi(self) -> None:
        """Поиграть с питомцем."""

    @abstractmethod
    def get_status(self) -> dict[str, int]:
        """Получить статус игры."""

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """Возвращает сумку с едой."""

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """Возвращает сумку с лекарствами."""


class Game(AbstractGame):
    """Простая реализация игры."""

    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine],
    ) -> None:
        """Создаёт игру с питомцем, кликером и магазином."""
        self.tamagochi = tamagochi
        self.clicker = clicker
        self._all_food = list(all_food)
        self._all_medicine = list(all_medicine)
        self._food_inventory: list[Food] = []
        self._medicine_inventory: list[Medicine] = []
        self._coins = 0

    @property
    def food(self) -> list[Food]:
        """Возвращает купленную еду."""
        return self._food_inventory

    @property
    def medicine(self) -> list[Medicine]:
        """Возвращает купленные лекарства."""
        return self._medicine_inventory

    def work(self) -> int:
        """Выполняет работу через кликер и возвращает доход."""
        self.clicker.click()
        income = self.clicker.income_per_click()
        self._coins += income
        return income

    def buy_food(self) -> None:
        """Покупает еду из доступного списка."""
        if not self._all_food:
            print("Нет доступной еды.")
            return

        print("Доступная еда:")
        for index, food in enumerate(self._all_food, start=1):
            print(
                f"{index}. {food.name} — насыщение {food.satiety}, "
                f"цена {food.price}"
            )

        try:
            choice = int(input("Выберите номер еды: "))
        except ValueError:
            print("Нужно ввести число.")
            return

        if not 1 <= choice <= len(self._all_food):
            print("Неверный номер.")
            return

        food = self._all_food[choice - 1]
        if self._coins < food.price:
            print(
                f"Недостаточно монет. Нужно {food.price}, "
                f"есть {self._coins}."
            )
            return

        self._coins -= food.price
        self._food_inventory.append(copy.deepcopy(food))
        print(f"Куплена еда: {food.name}.")

    def buy_medicine(self) -> None:
        """Покупает лекарство из доступного списка."""
        if not self._all_medicine:
            print("Нет доступных лекарств.")
            return

        print("Доступные лекарства:")
        for index, medicine in enumerate(self._all_medicine, start=1):
            print(
                f"{index}. {medicine.name} — лечение {medicine.heal_hp}, "
                f"использований {medicine.number_of_uses}, "
                f"цена {medicine.price}"
            )

        try:
            choice = int(input("Выберите номер лекарства: "))
        except ValueError:
            print("Нужно ввести число.")
            return

        if not 1 <= choice <= len(self._all_medicine):
            print("Неверный номер.")
            return

        medicine = self._all_medicine[choice - 1]
        if self._coins < medicine.price:
            print(
                f"Недостаточно монет. Нужно {medicine.price}, "
                f"есть {self._coins}."
            )
            return

        self._coins -= medicine.price
        self._medicine_inventory.append(copy.deepcopy(medicine))
        print(f"Куплено лекарство: {medicine.name}.")

    def _choose_food(self) -> Food | None:
        """Позволяет выбрать еду из сумки."""
        if not self._food_inventory:
            print("В сумке нет еды.")
            return None
        if len(self._food_inventory) == 1:
            return self._food_inventory[0]

        print("Выберите еду:")
        for index, food in enumerate(self._food_inventory, start=1):
            print(f"{index}. {food.name}")

        try:
            choice = int(input("Номер еды: "))
        except ValueError:
            print("Нужно ввести число.")
            return None

        if not 1 <= choice <= len(self._food_inventory):
            print("Неверный номер.")
            return None

        return self._food_inventory[choice - 1]

    def _choose_medicine(self) -> Medicine | None:
        """Позволяет выбрать лекарство из сумки."""
        if not self._medicine_inventory:
            print("В сумке нет лекарств.")
            return None
        if len(self._medicine_inventory) == 1:
            return self._medicine_inventory[0]

        print("Выберите лекарство:")
        for index, medicine in enumerate(self._medicine_inventory, start=1):
            left = medicine.number_of_uses - medicine.uses
            print(f"{index}. {medicine.name} (осталось использований: {left})")

        try:
            choice = int(input("Номер лекарства: "))
        except ValueError:
            print("Нужно ввести число.")
            return None

        if not 1 <= choice <= len(self._medicine_inventory):
            print("Неверный номер.")
            return None

        return self._medicine_inventory[choice - 1]

    def feed_tamagochi(self) -> None:
        """Кормит питомца выбранной едой."""
        food = self._choose_food()
        if food is None:
            return

        try:
            self.tamagochi.feed(food)
        except TamagochiDeadError as error:
            print(error)
            return

        self._food_inventory.remove(food)
        self.tamagochi.update()

    def heal_tamagochi(self) -> None:
        """Лечит питомца выбранным лекарством."""
        self._medicine_inventory = [
            medicine
            for medicine in self._medicine_inventory
            if not medicine.is_empty()
        ]
        medicine = self._choose_medicine()
        if medicine is None:
            return

        try:
            self.tamagochi.heal(medicine)
        except (TamagochiDeadError, MedicineEmptyError) as error:
            print(error)
            return

        if medicine.is_empty():
            self._medicine_inventory.remove(medicine)
        self.tamagochi.update()

    def rest_tamagochi(self) -> None:
        """Укладывает питомца отдыхать."""
        try:
            self.tamagochi.rest()
        except TamagochiDeadError as error:
            print(error)
            return
        self.tamagochi.update()

    def play_with_tamagochi(self) -> None:
        """Играет с питомцем."""
        try:
            self.tamagochi.play()
        except TamagochiDeadError as error:
            print(error)
            return
        self.tamagochi.update()

    def get_status(self) -> dict[str, int]:
        """Возвращает статус питомца и игры."""
        status = self.tamagochi.status()
        status["coins"] = self._coins
        return status


# Совместимость со старым именем
SimpleGame = Game
