from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states.fsm_states import StudentPlanSG
from keyboards.reply import get_main_menu
from keyboards.inline import get_confirm_keyboard

router = Router()

@router.message(F.text == "🎯 Создать план обучения")
async def start_plan_fsm(message: Message, state: FSMContext):
    await state.set_state(StudentPlanSG.goal)
    await message.answer("Введите вашу цель обучения (например: Сдать экзамен по Python на 90+):")

@router.message(StudentPlanSG.goal)
async def process_goal(message: Message, state: FSMContext):
    await state.update_data(goal=message.text)
    await state.set_state(StudentPlanSG.exam_date)
    await message.answer("Укажите дату экзамена в формате ГГГГ-ММ-ДД:")

@router.message(StudentPlanSG.exam_date)
async def process_exam_date(message: Message, state: FSMContext):
    await state.update_data(exam_date=message.text)
    await state.set_state(StudentPlanSG.days_per_week)
    await message.answer("Сколько дней в неделю вы готовы учиться? (1-7):")

@router.message(StudentPlanSG.days_per_week)
async def process_days_per_week(message: Message, state: FSMContext):
    await state.update_data(days_per_week=int(message.text))
    await state.set_state(StudentPlanSG.confirm)
    data = await state.get_data()
    await message.answer(
        f"Проверьте данные:\nЦель: {data['goal']}\nДата: {data['exam_date']}\nДней в неделю: {data['days_per_week']}",
        reply_markup=get_confirm_keyboard()
    )