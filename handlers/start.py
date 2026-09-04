from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

import database as db

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await db.get_or_create_user(message.from_user.id, message.from_user.username)
    await message.answer(
        "Привет! Я бот для работы с PDF-книгами.\n\n"
        "📄 Пришли мне PDF-файл — я сохраню его текст.\n"
        "❓ Потом просто пиши вопросы по книге — отвечу с помощью AI.\n"
        "📚 /mybooks — список твоих книг\n"
        "ℹ️ /help — помощь"
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "Как пользоваться:\n"
        "1. Отправь PDF-файл документом.\n"
        "2. После загрузки задавай вопросы по его содержимому обычным текстом.\n"
        "3. /mybooks — покажет все твои загруженные книги.\n"
        "4. Чтобы переключиться на другую книгу — используй /mybooks и выбери номер."
    )


@router.message(Command("mybooks"))
async def cmd_mybooks(message: Message):
    user_id = await db.get_or_create_user(message.from_user.id, message.from_user.username)
    books = await db.get_user_books(user_id)

    if not books:
        await message.answer("У тебя пока нет загруженных книг. Пришли PDF-файл.")
        return

    text_lines = ["Твои книги:\n"]
    for b in books:
        text_lines.append(f"#{b['id']} — {b['title']} ({b['uploaded_at'].strftime('%d.%m.%Y')})")
    text_lines.append("\nЧтобы сделать книгу активной для вопросов, напиши: /use (номер)")

    await message.answer("\n".join(text_lines))


@router.message(Command("use"))
async def cmd_use(message: Message):
    user_id = await db.get_or_create_user(message.from_user.id, message.from_user.username)
    parts = message.text.split()

    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("Использование: /use (номер книги) — посмотреть номера: /mybooks")
        return

    book_id = int(parts[1])
    books = await db.get_user_books(user_id)
    if not any(b["id"] == book_id for b in books):
        await message.answer("Книга с таким номером не найдена.")
        return

    await db.set_active_book(user_id, book_id)
    await message.answer(f"Готово, теперь активна книга #{book_id}. Можешь задавать вопросы.")
