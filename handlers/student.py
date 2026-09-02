from aiogram import F, Router
from aiogram.types import Message


router = Router()


@router.message(F.text == "Сегодняшний урок")
async def today_lesson(message: Message) -> None:
    await message.answer("Пока урок не создан. Сначала выберите программу обучения.")


@router.message(F.text == "План обучения")
async def learning_plan(message: Message) -> None:
    await message.answer("Здесь будет ваш персональный план обучения.")


@router.message(F.text == "Спросить ИИ")
async def ask_ai(message: Message) -> None:
    await message.answer("Напишите вопрос по текущей теме, и ИИ поможет с ответом.")


@router.message(F.text == "Прогресс")
async def progress(message: Message) -> None:
    await message.answer("Здесь будет статистика обучения и слабые темы.")
