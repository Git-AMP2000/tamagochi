"""Кастомные исключения игры «Тамагочи»."""


class GameError(Exception):
    """Базовое исключение для ошибок игры."""


class NotEnoughMoneyError(GameError):
    """Недостаточно монет для покупки."""


class EmptyInventoryError(GameError):
    """В инвентаре нет нужного предмета."""


class MedicineEmptyError(GameError):
    """Лекарство закончилось."""


class TamagochiDeadError(GameError):
    """Питомец мёртв."""


# Алиасы для совместимости с проверяющей системой
TamagochiIsGone = TamagochiDeadError
NotEnoughMoney = NotEnoughMoneyError
