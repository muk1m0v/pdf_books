from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


router = Router()


@router.message(Command("admin"))
async def admin_panel(message: Message) -> None:
    await message.answer("Панель администратора: создание программы и загрузка PDF.")
