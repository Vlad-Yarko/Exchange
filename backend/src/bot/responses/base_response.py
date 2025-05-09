from .response import MessageResponse
from ..messages.base_messages import *
from ..keyboard.reply.register_reply import register_keyboard
from ..fsm import RegisterState
from src.logger.logger import logger


router_logger = logger.make_router_logger('BASE')


class BaseMessageResponse(MessageResponse):
    async def start_hand(self):
        self.text = start_hand_message.render(username=self.message.from_user.username)
        await self.answer()

    async def help_hand(self):
        self.text = help_hand_message.render()
        await self.answer()

    async def register_hand(self):
        self.text = register_hand_message.render()
        self.keyboard = register_keyboard
        await self.state.set_state(RegisterState.active)
        await self.answer()
