# Импорт необходимых модулей
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
# Импорт листов из файла handlers/Messages.py
from ..handlers import Messages
# Импорт функций для работы с кнопками
from ..func import reg_func, menu_func
# Импорт модуля с функцией для его запуска
from ..handlers.Buying import get_buying_list
# Импорт нужного текста из файла interface/text.py
from ..interface.text import *
# Импорт клавиатуры с кнопками из файла interface/button.py
from ..interface.button import inline_kb


async def clear_state_and_messages(message: Message, state: FSMContext):
    """Очистка состояния и удаление сообщений."""
    await message.delete()
    await state.clear()
    await reg_func.delete_all_reg_menu_messages(message)
    await menu_func.delete_menu_registration(message)


async def repeat_reg_info(message: Message, state: FSMContext):
    """Повторное отображение меню 'Информация'."""
    with suppress(TelegramBadRequest):
        await clear_state_and_messages(message, state)
        info_message = await message.answer(information_text)
        Messages.menu_info.append(info_message.message_id)


async def repeat_reg_calc(message: Message, state: FSMContext):
    """Повторное отображение меню 'Рассчитать'."""
    with suppress(TelegramBadRequest):
        await clear_state_and_messages(message, state)
        menu_message = await message.answer(optional, reply_markup=inline_kb)
        Messages.menu_messages.append(menu_message.message_id)


async def repeat_reg_buy(message: Message, state: FSMContext):
    """Повторное отображение меню 'Купить'."""
    with suppress(TelegramBadRequest):
        await clear_state_and_messages(message, state)
        await get_buying_list(message)


async def handle_menu_actions(message: Message, state: FSMContext):
    """Обработка действий меню (Информация, Рассчитать, Купить)."""
    actions = {
        "Информация": repeat_reg_info,
        "Рассчитать": repeat_reg_calc,
        "Купить": repeat_reg_buy
    }

    if message.text in actions:
        await actions[message.text](message, state)
