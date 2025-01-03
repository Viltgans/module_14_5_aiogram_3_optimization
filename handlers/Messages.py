# Импорт необходимых модулей
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import html
from aiogram.fsm.context import FSMContext

# Импорт модулей основных меню с функциями
from ..func import menu_func, buy_menu_func, reg_func, calculator_func
# Импорт нужного текста из файла interface/text.py
from ..interface.text import optional, information_text, reg_text
# Импорт клавиатуры с кнопками из файла interface/button.py
from ..interface.button import inline_kb, kb
# Импорт модулей с функциями для их запуска
from ..handlers.Registration import start_registration
from ..handlers.Buying import get_buying_list

# Списки сообщений
pre_menu_messages = []
welcome_messages = []
menu_messages = []
menu_registr = []
menu_info = []
menu_buy = []

# Инициализация роутера
router = Router()


# Функция команды /start
@router.message(CommandStart())
async def start(message: Message):
    with suppress(TelegramBadRequest):
        # Удаление сообщения /start
        await message.delete()
        # Удаление всех сообщений, которые были отправлены до команды /start
        await menu_func.delete_pre_menu_messages(message)
        # Приветственное сообщение при команде /start
        welcome_message = await message.answer(
            f'Здравствуйте, {html.bold(html.quote(message.from_user.full_name))}! '
            f'Я бот помогающий здоровью.', parse_mode='HTML', reply_markup=kb
        )
        welcome_messages.append(welcome_message.message_id)


# Функция кнопки "Рассчитать"
@router.message(F.text == "Рассчитать")
async def sing_up(message: Message):
    with suppress(TelegramBadRequest):
        # Удаление сообщения "Рассчитать"
        await message.delete()
        # Удаление всех сообщений, которые были отправлены до кнопки "Рассчитать"
        await menu_func.delete_pre_menu_messages(message)
        # Удаление всех сообщений кнопки 'Информация'
        await menu_func.delete_menu_information(message)
        # Удаление всех сообщений кнопки 'Регистрация'
        await menu_func.delete_menu_registration(message)
        await reg_func.delete_all_reg_menu_messages(message)
        # Удаление всех сообщений кнопки 'Купить'
        await menu_func.delete_menu_buy(message)
        await buy_menu_func.delete_all_buy_menu_messages(message)
        # Инициализация
        menu_message = await message.answer(optional, reply_markup=inline_kb)
        menu_messages.append(menu_message.message_id)


# Функция кнопки "Информация"
@router.message(F.text == "Информация")
async def information(message: Message):
    with suppress(TelegramBadRequest):
        # Удаление сообщения "Информация"
        await message.delete()
        # Удаление всех сообщений, которые были отправлены до кнопки "Информация"
        await menu_func.delete_pre_menu_messages(message)
        # Удаление всех сообщений кнопки 'Рассчитать'
        await menu_func.delete_menu_calc_and_formula(message)
        await calculator_func.delete_all_menu_calc_and_formula(message)
        # Удаление всех сообщений кнопки 'Регистрация'
        await menu_func.delete_menu_registration(message)
        await reg_func.delete_all_reg_menu_messages(message)
        # Удаление всех сообщений кнопки 'Купить'
        await menu_func.delete_menu_buy(message)
        await buy_menu_func.delete_all_buy_menu_messages(message)
        # Удаление всех подменю кнопки 'Рассчитать'
        await calculator_func.delete_submenu_calc_and_formula(message)
        # Инициализация
        info_message = await message.answer(information_text)
        menu_info.append(info_message.message_id)


# Функция кнопки "Регистрация"
@router.message(F.text == "Регистрация")
async def registration_menu(message: Message, state: FSMContext):
    with suppress(TelegramBadRequest):
        # Удаление сообщения "Регистрация"
        await message.delete()
        # Удаление всех сообщений, которые были отправлены до кнопки "Регистрация"
        await menu_func.delete_pre_menu_messages(message)
        # Удаление всех сообщений кнопки 'Информация'
        await menu_func.delete_menu_information(message)
        # Удаление всех сообщений кнопки 'Рассчитать'
        await menu_func.delete_menu_calc_and_formula(message)
        await calculator_func.delete_all_menu_calc_and_formula(message)
        # Удаление всех сообщений кнопки 'Купить'
        await menu_func.delete_menu_buy(message)
        await buy_menu_func.delete_all_buy_menu_messages(message)
        # Удаление всех подменю кнопки 'Рассчитать'
        await calculator_func.delete_submenu_calc_and_formula(message)
        # Инициализация
        reg_message = await message.answer(reg_text)
        menu_registr.append(reg_message.message_id)
        await start_registration(message, state)


# Функция кнопки "Купить"
@router.message(F.text == "Купить")
async def buying_menu(message: Message):
    with suppress(TelegramBadRequest):
        # Удаление сообщения "Купить"
        await message.delete()
        # Удаление всех сообщений, которые были отправлены до кнопки "Купить"
        await menu_func.delete_pre_menu_messages(message)
        # Удаление всех сообщений кнопки 'Информация'
        await menu_func.delete_menu_information(message)
        # Удаление всех сообщений кнопки 'Рассчитать'
        await menu_func.delete_menu_calc_and_formula(message)
        await calculator_func.delete_all_menu_calc_and_formula(message)
        # Удаление всех сообщений кнопки 'Регистрация'
        await menu_func.delete_menu_registration(message)
        await reg_func.delete_all_reg_menu_messages(message)
        # Удаление всех подменю кнопки 'Рассчитать'
        await calculator_func.delete_submenu_calc_and_formula(message)
        # Инициализация
        await get_buying_list(message)


# Функция всех сообщений
@router.message(F.text)
async def all_massages(message: Message):
    with suppress(TelegramBadRequest):
        # Удаление всех сообщений не соответствующих команде /start
        await message.delete()
        # Если список сообщений пуст по длине списка, то вывести его и добавить в список
        if len(pre_menu_messages) == 0:
            # Сообщение о необходимости ввести команду /start
            message = await message.answer(f'{html.bold(html.quote(message.from_user.full_name))}! '
                                           f'Введите команду /start, чтобы начать общение.', parse_mode='HTML')
            pre_menu_messages.append(message.message_id)
        # Если список сообщений не пуст по длине списка, то ничего не делать
        if len(pre_menu_messages) > 1:
            return
