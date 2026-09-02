from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.reply import main_menu_keyboard


router = Router()


@router.message(CommandStart())
async def start_command(message: Message) -> None:
    await message.answer(
        "Привет! Я помогу составить план обучения и готовиться к экзамену.",
        reply_markup=main_menu_keyboard(),
    )
