from sqlalchemy.ext.asyncio import AsyncSession

from .response import MessageResponse
from ..messages.register_messages import *
from src.databases.models.tg_user import TelegramUser
from src.logger.logger import logger


router_logger = logger.make_router_logger('REGISTER')


class RegisterMessageResponse(MessageResponse):
    async def register_contact_hand(self, session: AsyncSession) -> None:
        chat_id = self.message.chat.id
        user = await TelegramUser.is_user_by_chat_id(session, chat_id)
        if user:
            self.text = register_error.render()
        else:
            await TelegramUser.register_tg_user(
                session,
                chat_id=chat_id,
                phone_number=self.message.contact.phone_number.strip('+')
            )
            self.text = register_success.render()

        await self.state.clear()
        await self.answer()
