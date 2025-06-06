import logging
import random

from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from .finance_db import FinanceDb


"""
С помощь конечных автоматов ведем диалог с пользователем для получения
текста расхода и суммы. По пути пользователь также выбирает категорию,
которую мы храним в State().

Мне не нравится взаимодействие с бд. Надо это пофикстить.
Убрать создание бд. Или вообще или в этом файле точно.
Каждый раз не нужно ее вызывать.

В функции retrive_data поменять вывод. Не использовать индексы.

Также можно улучшить сам механизм добавления и получения данных
с бд. Может использовать именованные кортежи?
"""


CATEGORIES = ('Еда', 'Одежда', 'Техника', 'Различные товары')

router = Router()
db = FinanceDb()

# BASE_DIR = Path(__file__).resolve().parent


class EnterExpenses(StatesGroup):
    enter_text = State()
    enter_money = State()
    category = State()


@router.message(Command('MenuList'))
async def show_menu(message: types.Message):
    """Function for displaying menu.

    For now only two options - Внести расходы and Показать расходы.
    """
    logging.info('Starting display commands in show_menu function')
    keyboard = [
        [
            types.KeyboardButton(text='Внести расходы'),
            types.KeyboardButton(text='Показать расходы'),
        ]
    ]
    keyboard_for_reply = types.ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder='Выберите функцию.'
    )
    await message.answer(
        'Выберите команду',
        reply_markup=keyboard_for_reply,
        one_time_keyboard=True
    )


@router.message(F.text == 'Внести расходы')
async def choice_category(message: types.Message):
    """Function for displaying categories.
    """
    logging.info('Start display choice_category function')
    keyboard = [[types.KeyboardButton(text=text)] for text in CATEGORIES]
    keyboard_for_reply = types.ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )
    await message.answer(
        'Выберите категорию',
        reply_markup=keyboard_for_reply,
        one_time_keyboard=True,
    )


@router.message(StateFilter(None), F.text.in_(CATEGORIES))
async def get_text_expense(message: types.Message, state: FSMContext):
    """Function for writing user's record in database.
    """
    logging.info('Start display write_records_in_db function')
    await state.update_data(category=message.text)
    await message.answer(
        'Введите текст расхода:',
    )
    await state.set_state(EnterExpenses.enter_text)


@router.message(
    EnterExpenses.enter_text,
)
async def get_money_expense(message: types.Message, state: FSMContext):
    await state.update_data(enter_text=message.text.lower())
    await message.answer(
        text=f"Вы ввели {message.text}, теперь введите сумму:",
    )
    await state.set_state(EnterExpenses.enter_money)


@router.message(EnterExpenses.enter_money)
async def adding_data_to_db(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        text=f"Вы ввели {user_data['enter_text']} с затратами {message.text}."
    )
    db.create_table()  # NEED REMOVE THIS
    db.adding_data(
        user_data['enter_text'],
        float(message.text),
        user_data['category']
    )
    await state.clear()


@router.message(F.text == 'Показать расходы')
async def retrive_data(message: types.Message):
    data = db.retrive_data()
    if data is None:
        await message.answer('No data')
        return
    result_string = ''
    for info in data:
        result_string += (
            f'Название расхода: {info[0]},'
            f'категория: {info[2]}, сумма {str(info[1])} \n')
    await message.answer(result_string)
