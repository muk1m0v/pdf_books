from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_confirm_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура подтверждения в FSM"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_plan"),
                InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_plan")
            ]
        ]
    )

def get_lesson_action_keyboard(plan_day_id: int) -> InlineKeyboardMarkup:
    """Кнопки действия в рамках урока"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📝 Пройти тест", callback_data=f"start_quiz_{plan_day_id}")],
            [InlineKeyboardButton(text="❓ Вопрос к AI", callback_data=f"ask_ai_{plan_day_id}")],
            [
                InlineKeyboardButton(text="⏩ Перенести урок", callback_data=f"reschedule_{plan_day_id}"),
                InlineKeyboardButton(text="🚫 Пропустить", callback_data=f"skip_{plan_day_id}")
            ]
        ]
    )

def get_quiz_options_keyboard(question_id: int, options: list[str]) -> InlineKeyboardMarkup:
    """Генерация кнопок с вариантами ответов для теста"""
    buttons = []
    for idx, option in enumerate(options):
        buttons.append([
            InlineKeyboardButton(
                text=f"{idx + 1}. {option}", 
                callback_data=f"quiz_ans_{question_id}_{idx}"
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)