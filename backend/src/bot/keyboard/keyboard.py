from abc import ABC, abstractmethod

from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup


class Keyboard(ABC):
    def __init__(self, buttons):
        self.buttons = buttons

    @abstractmethod
    def make_keyboard(self):
        pass


class InlineKeyboard(Keyboard):
    def make_keyboard(self):
        return InlineKeyboardMarkup(inline_keyboard=self.buttons)


class ReplyKeyboard(Keyboard):
    def make_keyboard(self):
        return ReplyKeyboardMarkup(keyboard=self.buttons, resize_keyboard=True, one_time_keyboard=True)
