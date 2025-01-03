# Импорт необходимых модулей
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

# Импорт листов из файла handlers/Messages.py и handlers/Calculator.py
from ..handlers import Messages, Calculator


# Общая функция для удаления сообщений из списка
async def delete_messages(message: Message, message_list: list, clear_list: bool = True):
    with suppress(TelegramBadRequest):
        for msg_id in message_list:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=msg_id)
        if clear_list:
            message_list.clear()


# Функция для удаления сообщений предшествующих меню
async def delete_pre_menu_messages(message: Message):
    await delete_messages(message, Messages.pre_menu_messages, clear_list=False)


# Функция для удаления приветственного сообщения
async def delete_welcome_messages(message: Message):
    await delete_messages(message, Messages.welcome_messages)


# Функция для удаления сообщений меню 'Информация'
async def delete_menu_information(message: Message):
    await delete_messages(message, Messages.menu_info)


# Функция для удаления сообщений меню 'Рассчитать'
async def delete_menu_calc_and_formula(message: Message):
    await delete_messages(message, Messages.menu_messages)


# Функция для удаления сообщений меню 'Регистрация'
async def delete_menu_registration(message: Message):
    await delete_messages(message, Messages.menu_registr)


# Функция для удаления сообщений меню 'Купить'
async def delete_menu_buy(message: Message):
    await delete_messages(message, Messages.menu_buy)


# Функция для удаления сообщений подменю 'Рассчитать' в обратном порядке
async def delete_all_menu_messages(message: Message):
    chat_id = message.chat.id
    lists_to_clear = [
        Calculator.formulas,
        Calculator.calories,
        Calculator.messages_man,
        Calculator.messages_woman,
        Calculator.messages,
        Calculator.results
    ]

    for message_list in lists_to_clear:
        await delete_messages(message, message_list[::-1])
