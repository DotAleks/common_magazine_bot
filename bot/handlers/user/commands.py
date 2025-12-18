from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import CommandStart

from core.strings import CMD_START_MESSAGE
from bot.keyboards import get_main_kb


router = Router(name='user_commands')

@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(text=CMD_START_MESSAGE,reply_markup=get_main_kb())