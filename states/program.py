from aiogram.fsm.state import State, StatesGroup


class ProgramStates(StatesGroup):
    title = State()
    description = State()
    pdf_upload = State()
    confirmation = State()
