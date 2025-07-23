import logging

from aiogram import Router, types
from aiogram.filters import Command


router = Router()


@router.message(Command('start', 'help'))
async def return_help_message(message: types.Message):
    """
    Function that show help message for user.
    """
    logging.info('Starting function with help command')
    help_message = """
    Для выбора действия введите или нажмите на /menulist.
    При внисении расхода необходимо будет выбрать или\n
    ввести категорию, затем ввести текст расхода и сумму расхода.

    Вывод расходов будет в таком виде:
    <id расхода>. <Название расхода>:
    Категория: <Название категории>
    Сумма: <Сумма расхода>
    Время: <Время расхода>:

    В конце будет указана: Общая сумма расхода
    Если вы ошиблись при вводе данных, то напишите отмена
    """
    await message.answer(help_message, parse_mode='')
