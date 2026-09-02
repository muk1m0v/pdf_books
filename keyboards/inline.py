from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def confirm_keyboard(prefix: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Подтвердить", callback_data=f"{prefix}:confirm"),
                InlineKeyboardButton(text="Отмена", callback_data=f"{prefix}:cancel"),
            ]
        ]
    )
