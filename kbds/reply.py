from aiogram.types import KeyboardButton, ReplyKeyboardRemove, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


CATEGORIES = ('Еда', 'Одежда', 'Техника', 'Прочее')
DATA_RETRIVE_CHOICES = (
    'За сегодня', 'За этот месяц', 'За прошлый месяц', 'За всё время',
    'По категориям'
)

menu_keyboard = ReplyKeyboardBuilder()
menu_keyboard.add(
    KeyboardButton(text='Внести расходы'),
    KeyboardButton(text='Показать расходы'),
    KeyboardButton(text='Удалить расход'),
)

catogories_keyboard = ReplyKeyboardBuilder()
catogories_keyboard.add(
    *[KeyboardButton(text=text) for text in CATEGORIES]
)
catogories_keyboard.adjust(2)

show_expenses_keyboard = ReplyKeyboardBuilder()
show_expenses_keyboard.add(
    *[KeyboardButton(text=text) for text in DATA_RETRIVE_CHOICES]
)
show_expenses_keyboard.adjust(2)
