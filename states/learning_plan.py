from aiogram.fsm.state import State, StatesGroup


class LearningPlanStates(StatesGroup):
    goal = State()
    deadline = State()
    study_days = State()
    session_time = State()
    session_duration = State()
    level = State()
