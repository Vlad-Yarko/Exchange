from aiogram import Router
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from ..responses.special_response import SpecialMessageResponse
from ..filters.special_filter import QuitFilter


router = Router()
router.message.filter(StateFilter('*'))


@router.message(QuitFilter())
async def quit_hand(message: Message, state: FSMContext):
    await SpecialMessageResponse(
        message=message,
        state=state
    ).quit_hand()
