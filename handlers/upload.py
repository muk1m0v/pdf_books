from aiogram import Router, F, Bot
from aiogram.types import Message

import database as db
from pdf_utils import extract_text_from_pdf

router = Router()


@router.message(F.document)
async def handle_pdf(message: Message, bot: Bot):
    document = message.document

    if not (document.mime_type == "application/pdf" or document.file_name.lower().endswith(".pdf")):
        await message.answer("Это не PDF. Пришли, пожалуйста, файл в формате .pdf")
        return

    status_msg = await message.answer("Обрабатываю PDF, подожди немного...")

    file = await bot.get_file(document.file_id)
    file_bytes_io = await bot.download_file(file.file_path)
    file_bytes = file_bytes_io.read()

    text = extract_text_from_pdf(file_bytes)

    if not text.strip():
        await status_msg.edit_text(
            "Не удалось извлечь текст из этого PDF (возможно, это скан-изображение без текстового слоя)."
        )
        return

    user_id = await db.get_or_create_user(message.from_user.id, message.from_user.username)
    title = document.file_name or "Без названия"
    book_id = await db.save_book(user_id, title, text)

    await status_msg.edit_text(
        f"Книга «{title}» загружена и сохранена (#{book_id}).\n"
        f"Теперь просто напиши вопрос по её содержимому!"
    )
