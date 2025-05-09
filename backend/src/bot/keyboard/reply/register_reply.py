from ..keyboard import ReplyKeyboard
from ..button import ContactButton, ReplyButton


register_keyboard = ReplyKeyboard(
    [
        [
            ContactButton('Share phone number').button
        ],
        [
            ReplyButton('quit').button
        ]
    ]
).make_keyboard()
