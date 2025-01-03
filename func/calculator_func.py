# Импорт необходимых модулей
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery

# Импорт листов из файла handlers/Calculator.py
from ..handlers import Calculator


# Общая функция для удаления сообщений
async def delete_messages(chat_id, message_ids, bot):
    with suppress(TelegramBadRequest):
        for msg_id in message_ids:
            try:
                await bot.delete_message(chat_id=chat_id, message_id=msg_id)
            except Exception as e:
                print(f"Ошибка: {e}")
        message_ids.clear()


# Функция для удаления сообщений в меню 'Рассчитать' при аргументе Message
async def delete_all_menu_calc_and_formula(message: Message):
    await delete_messages(message.chat.id, Calculator.messages, message.bot)


# Функция для удаления сообщений в подменю 'Рассчитать' при аргументе Message
async def delete_submenu_calc_and_formula(message: Message):
    await delete_messages(message.chat.id, Calculator.formulas, message.bot)
    await delete_messages(message.chat.id, Calculator.messages_man, message.bot)
    await delete_messages(message.chat.id, Calculator.messages_woman, message.bot)
    Calculator.calories.clear()


# Функция для удаления сообщений в меню 'Рассчитать'
# подменю inline-кнопки 'Рассчитать норму калорий' при расчете нормы калорий
# для вывода полученной информации от пользователя при аргументе CallbackQuery
async def delete_messages_callback(callback: CallbackQuery):
    await delete_messages(callback.message.chat.id, Calculator.messages_input, callback.bot)


# Функция для удаления сообщений в меню 'Рассчитать'
# подменю inline-кнопки 'Рассчитать норму калорий' при расчете нормы калорий
# для мужчин при аргументе CallbackQuery
async def delete_man_messages(callback: CallbackQuery):
    await delete_messages(callback.message.chat.id, Calculator.messages_man, callback.bot)


# Функция для удаления сообщений в меню 'Рассчитать'
# подменю inline-кнопки 'Рассчитать норму калорий' при расчете нормы калорий
# для женщин при аргументе CallbackQuery
async def delete_woman_messages(callback: CallbackQuery):
    await delete_messages(callback.message.chat.id, Calculator.messages_woman, callback.bot)


# Функция для удаления сообщений результатов в меню 'Рассчитать'
# подменю inline-кнопки 'Рассчитать норму калорий' при расчете нормы калорий
# при аргументе CallbackQuery
async def delete_result_messages(callback: CallbackQuery):
    await delete_messages(callback.message.chat.id, Calculator.results, callback.bot)


# Функция для удаления сообщений в меню 'Рассчитать'
# подменю inline-кнопки 'Формулы расчёта' при аргументе CallbackQuery
async def delete_formulas(callback: CallbackQuery):
    await delete_messages(callback.message.chat.id, Calculator.formulas, callback.bot)


# Функция для удаления сообщений результатов в меню 'Рассчитать'
# подменю inline-кнопки 'Рассчитать норму калорий'
async def delete_calories(callback: CallbackQuery):
    await delete_messages(callback.message.chat.id, Calculator.calories, callback.bot)
