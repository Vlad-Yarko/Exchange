from .response import MessageResponse
from ..messages.special_messages import *
from src.logger.logger import logger


router_logger = logger.make_router_logger('SPECIAL')


class SpecialMessageResponse(MessageResponse):
    async def quit_hand(self):
        st = await self.state.get_state()
        if st is not None:
            await self.state.clear()
            self.text = quit_hand_message.render()
            self.keyboard = {"remove_keyboard": True}
            await self.answer()
