from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def make_keyboard(*btns, sizes=(2,), placeholder='Выберите функцию'):
    """
    Function for creating keyboards.
    """
    keyboard_builder = ReplyKeyboardBuilder()
    for text in btns:
        keyboard_builder.add(KeyboardButton(text=text))
    return keyboard_builder.adjust(*sizes).as_markup(
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder=placeholder
    )
