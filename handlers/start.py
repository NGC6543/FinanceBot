import logging

from aiogram import F, Router, types
from aiogram.filters import Command


router = Router()


@router.message(Command('help'))
async def return_help_message(message: types.Message):
    logging.info('Starting function with help command')
    help_message = """
    Для ввода расходов следуйте инструкции по вводу расхода.

    Вывод расходов будет в таком виде:
    <id расхода>. <Название расхода>:
    Категория: <Название категории>
    Сумма: <Сумма расхода>
    Время: <Время расхода>:

    В конце будет указана: Общая сумма расхода"""
    await message.answer(help_message, parse_mode='')
