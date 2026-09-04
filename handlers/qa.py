from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

import handlers.database as db
from ai_service import ask_about_book

router = Router()


@router.message(F.text & ~F.text.startswith("/"))
async def handle_question(message: Message):
    user_id = await db.get_or_create_user(message.from_user.id, message.from_user.username)
    book = await db.get_active_book(user_id)

    if not book:
        await message.answer("Сначала пришли PDF-файл книги, потом задавай вопросы.")
        return

    thinking_msg = await message.answer("Думаю над ответом...")

    answer = await ask_about_book(message.text, book["title"], book["content"])

    await thinking_msg.edit_text(answer)
