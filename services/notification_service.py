from aiogram import Bot


async def send_lesson_reminder(bot: Bot, telegram_id: int, text: str) -> None:
    await bot.send_message(chat_id=telegram_id, text=text)
