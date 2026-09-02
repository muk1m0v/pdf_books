from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="Сегодняшний урок"), KeyboardButton(text="План обучения")],
        [KeyboardButton(text="Спросить ИИ"), KeyboardButton(text="Прогресс")],
        [KeyboardButton(text="Практика"), KeyboardButton(text="Настройки")],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
