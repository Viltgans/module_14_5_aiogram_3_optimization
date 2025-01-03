# Импорт необходимых модулей
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
# Импорт модуля menu_func с функциями из папки func
from ..func import menu_func
# Импорт функций из файла func/calculator_func.py
from ..func import calculator_func
# Импорт нужного текста из файла interface/text.py
from ..interface.text import *
# Импорт модулей с функциями для их запуска
from ..handlers import Registration, Buying, Messages


async def clear_state_and_messages(message: Message, state: FSMContext):
    """Очистка состояния и удаление сообщений."""
    with suppress(TelegramBadRequest):
        await message.delete()
        await state.clear()
        await menu_func.delete_menu_calc_and_formula(message)
        await calculator_func.delete_all_menu_calc_and_formula(message)
        await menu_func.delete_all_menu_messages(message)


async def repeat_calc_info(message: Message, state: FSMContext):
    """Обработка кнопки 'Информация'."""
    await clear_state_and_messages(message, state)
    info_message = await message.answer(information_text)
    Messages.menu_info.append(info_message.message_id)


async def repeat_calc_reg(message: Message, state: FSMContext):
    """Обработка кнопки 'Регистрация'."""
    await clear_state_and_messages(message, state)
    info_message = await message.answer(reg_text)
    Messages.menu_registr.append(info_message.message_id)
    await Registration.start_registration(message, state)


async def repeat_calc_buy(message: Message, state: FSMContext):
    """Обработка кнопки 'Купить'."""
    await clear_state_and_messages(message, state)
    await Buying.get_buying_list(message)


async def handle_menu_actions(message: Message, state: FSMContext):
    """Обработка действий меню (Информация, Рассчитать, Купить)."""
    actions = {
        "Информация": repeat_calc_info,
        "Рассчитать": repeat_calc_reg,
        "Купить": repeat_calc_buy
    }

    if message.text in actions:
        await actions[message.text](message, state)
