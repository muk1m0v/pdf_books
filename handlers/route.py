from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from database.db import get_connection
from handlers.student import router as student_router
from keyboards.reply import get_main_menu

router = Router()


async def upsert_user(message: Message, role: str = "student") -> None:
    conn = await get_connection()
    if not conn:
        return

    full_name = message.from_user.full_name if message.from_user else "Unknown user"
    telegram_id = message.from_user.id if message.from_user else message.chat.id

    try:
        await conn.execute(
            """
            INSERT INTO users (telegram_id, full_name, role)
            VALUES ($1, $2, $3)
            ON CONFLICT (telegram_id)
            DO UPDATE SET
                full_name = EXCLUDED.full_name,
                role = COALESCE(users.role, EXCLUDED.role);
            """,
            telegram_id,
            full_name,
            role,
        )
    finally:
        await conn.close()


@router.message(CommandStart())
async def start_command(message: Message) -> None:
    await upsert_user(message)
    await message.answer(
        "Привет! Я помогу составить учебный план, пройти уроки и смотреть прогресс.",
        reply_markup=get_main_menu("student"),
    )


@router.message(Command("help"))
async def help_command(message: Message) -> None:
    await message.answer(
        "Доступные команды:\n"
        "/start - регистрация и главное меню\n"
        "/menu - открыть главное меню\n"
        "/help - помощь"
    )


@router.message(Command("menu"))
@router.message(F.text == "Меню")
async def menu_command(message: Message) -> None:
    await message.answer(
        "Главное меню:",
        reply_markup=get_main_menu("student"),
    )


@router.message(F.text.casefold() == "привет")
async def hello_message(message: Message) -> None:
    await message.answer(
        "Привет! Нажми кнопку в меню или напиши /help.",
        reply_markup=get_main_menu("student"),
    )


router.include_router(student_router)
