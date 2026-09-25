"""Пакет игры «Тамагочи»."""

from .clicker import AbstractClicker, Clicker, SimpleRandomClicker
from .game import AbstractGame, Game, SimpleGame
from .models import Food, Medicine
from .tamagochi import AbstractTamagochi, SimpleTamagochi, Tamagochi

__all__ = [
    "AbstractClicker",
    "AbstractGame",
    "AbstractTamagochi",
    "Clicker",
    "Food",
    "Game",
    "Medicine",
    "SimpleGame",
    "SimpleRandomClicker",
    "SimpleTamagochi",
    "Tamagochi",
]
