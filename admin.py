import asyncio

from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message

import database as db
from config import ADMIN_IDS

router = Router()


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


@router.message(Command("stats"))
async def cmd_stats(message: Message):
    if not is_admin(message.from_user.id):
        return 

    stats = await db.get_stats()
    await message.answer(
        "📊 Статистика бота:\n\n"
        f"Пользователей: {stats['users']}\n"
        f"Загружено книг: {stats['books']}"
    )


@router.message(Command("broadcast"))
async def cmd_broadcast(message: Message, bot: Bot):
    if not is_admin(message.from_user.id):
        return

    text = message.text.replace("/broadcast", "", 1).strip()
    if not text:
        await message.answer("Использование: /broadcast (текст сообщения)")
        return

    tg_ids = await db.get_all_user_tg_ids()
    status_msg = await message.answer(f"Рассылаю на {len(tg_ids)} пользователей...")

    sent = 0
    failed = 0
    for tg_id in tg_ids:
        try:
            await bot.send_message(tg_id, text)
            sent += 1
        except Exception:
            failed += 1
        await asyncio.sleep(0.05)

    await status_msg.edit_text(f"Готово. Доставлено: {sent}, не доставлено: {failed}")