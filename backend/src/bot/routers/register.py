from aiogram import Router
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from ..responses.register_response import RegisterMessageResponse
from ..fsm import RegisterState
from ..filters.register_filter import RegisterStateFilter, ContactFilter


router = Router()
router.message.filter(StateFilter(RegisterState))


@router.message(RegisterStateFilter('active'), ContactFilter())
async def register_contact_hand(message: Message, state: FSMContext, session: AsyncSession):
    await RegisterMessageResponse(
        message=message,
        state=state
    ).register_contact_hand(session)
