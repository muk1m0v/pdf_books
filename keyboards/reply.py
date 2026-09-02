from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu(role: str = "student") -> ReplyKeyboardMarkup:
    """Главное меню для студента или администратора"""
    if role == "admin":
        buttons = [
            [KeyboardButton(text="📚 Управление программами"), KeyboardButton(text="📄 Загрузить PDF")],
            [KeyboardButton(text="👥 Список студентов"), KeyboardButton(text="📊 Аналитика")]
        ]
    else:
        buttons = [
            [KeyboardButton(text="📖 Сегодняшний урок"), KeyboardButton(text="🎯 Создать план обучения")],
            [KeyboardButton(text="❓ Задать вопрос AI"), KeyboardButton(text="📊 Мой прогресс")],
            [KeyboardButton(text="📝 Пробный экзамен")]
        ]
    
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        persistent=True
    )