import logging

from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from .finance_db import FinanceDb


"""
С помощь конечных автоматов ведем диалог с пользователем для получения
текста расхода и суммы. По пути пользователь также выбирает категорию,
которую мы храним в State().

Сделать cursor и connect как декоратор для работы с бд?
"""


CATEGORIES = ('Еда', 'Одежда', 'Техника', 'Различные товары')
DATA_RETRIVE_CHOICES = (
    'За сегодня', 'За этот месяц', 'За прошлый месяц', 'За всё время',
    'По категориям'
)

router = Router()
db = FinanceDb()
db.create_table()


class EnterExpenses(StatesGroup):
    enter_text = State()
    enter_money = State()
    category = State()


async def get_data(data, message):
    if not data:
        await message.answer(f'За период {message.text} данных не было.')
        return
    result_string = ''
    total_sum = 0
    for info in data:
        # if 
        result_string += (
            f'Название расхода: {info[0]}, '
            f'Категория: {info[2]}, Сумма {str(info[1])} \n')
        total_sum += info[1]
    result_string += f'Общая сумма: {total_sum}'
    await message.answer(result_string)


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
    """Function for getting user's text.
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
    """Function for getting user's money.
    """
    await state.update_data(enter_text=message.text.lower())
    await message.answer(
        text=f"Вы ввели {message.text}, теперь введите сумму:",
    )
    await state.set_state(EnterExpenses.enter_money)


@router.message(EnterExpenses.enter_money)
async def adding_data_to_db(message: types.Message, state: FSMContext):
    """Function for adding user's expense.
    """
    user_data = await state.get_data()
    await message.answer(
        text=f"Вы ввели: {user_data['enter_text']} с затратами {message.text}."
    )
    db.adding_data(
        user_data['enter_text'],
        float(message.text),
        user_data['category']
    )
    await state.clear()
    await show_menu(message)


@router.message(F.text == 'Показать расходы')
async def retrive_data(message: types.Message):
    """Function for user's choices date.
    """
    logging.info('Start retrive_data function')
    keyboard = [
        [types.KeyboardButton(text=text)] for text in DATA_RETRIVE_CHOICES
    ]
    keyboard_for_reply = types.ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )
    await message.answer(
        'Выберите за какой период показать данные.',
        reply_markup=keyboard_for_reply,
        one_time_keyboard=True,
    )


@router.message(F.text == 'По категориям')
async def get_data_by_category(message: types.Message):
    """Function for getting data group by a category.
    """
    logging.info('Start get_data_by_category function')
    data = db.retrive_data_by_category()
    if not data:
        await message.answer(f'За период {message.text} данных не было.')
        return
    result_string = 'За этот месяц расходы по категориям: \n'
    total_sum = 0
    for info in data:
        result_string += (
            f'Категория: {info.category}, Сумма {str(info.money)} \n')
        total_sum += info[0]
    result_string += f'Общая сумма: {total_sum}'
    await message.answer(result_string)


@router.message(F.text.in_(DATA_RETRIVE_CHOICES))
async def get_date_with_range(message: types.Message):
    """Function for getting data with a specific date.
    """
    logging.info('Start get_date_range function')
    data = db.retrive_data_by_date(message.text)
    if not data:
        await message.answer(f'За период {message.text} данных не было.')
        return
    result_string = ''
    total_sum = 0
    for info in data:
        result_string += (
            f'Название расхода: {info.text}, '
            f'Категория: {info.category}, Сумма {str(info.money)} \n')
        total_sum += info[1]
    result_string += f'Общая сумма: {total_sum}'
    await message.answer(result_string)
