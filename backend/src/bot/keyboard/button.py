from abc import ABC, abstractmethod

from aiogram.types import InlineKeyboardButton, KeyboardButton


class Button(ABC):
    @abstractmethod
    def __init__(self):
        pass


class CallbackButton(Button):
    def __init__(self, text, callback):
        self.text = text
        self.callback = callback
        self.button = InlineKeyboardButton(text=self.text, callback_data=self.callback)


class UrlButton(Button):
    def __init__(self, text, url):
        self.text = text
        self.url = url
        self.button = InlineKeyboardButton(text=self.text, url=self.url)


class ContactButton(Button):
    def __init__(self, text):
        self.text = text
        self.button = KeyboardButton(text=self.text, request_contact=True)


class ReplyButton(Button):
    def __init__(self, text):
        self.text = text
        self.button = KeyboardButton(text=self.text)
