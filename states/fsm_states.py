from aiogram.fsm.state import StatesGroup, State

class StudentPlanSG(StatesGroup):
    goal = State()
    exam_date = State()
    days_per_week = State()
    study_days = State()
    duration = State()
    study_time = State()
    current_level = State()
    confirm = State()

class AdminAddMaterialSG(StatesGroup):
    title = State()
    description = State()
    pdf_file = State()
    confirm = State()

class QuestionAISG(StatesGroup):
    asking = State()