# Импорт необходимых модулей
import re
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

# Импорт модулей с функциями из папки func, чтобы избавиться от дублирования кода
from ..func import repeat_reg
# Импорт функций для работы с базой данных
from ..database.data_user import *
# Импорт функций для работы с кнопками
from ..func import reg_func
# Импорт нужного текста из файла interface/text.py
from ..interface.text import *
# Импорт функций из файла func/menu_func.py
from ..func import menu_func

# Инициализация роутера
router = Router()


# Инициализация машины состояний для регистрации пользователя
class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()


# Инициализация списков для хранения сообщений
reg_messages = []
user_info = []
reg_results = []


# Функция кнопки 'Регистрация'
# Получение значения имени пользователя
async def start_registration(message: Message, state: FSMContext):
    with suppress(TelegramBadRequest):
        # Инициализация
        reg_message = await message.answer(name_input)
        reg_messages.append(reg_message.message_id)
        await state.set_state(RegistrationState.username)


# Функция кнопки 'Регистрация'
# Обработка значения имени пользователя и добавление его в БД
@router.message(RegistrationState.username)
async def set_username(message: Message, state: FSMContext):
    with suppress(TelegramBadRequest):
        # Инициализация
        username_input = message.text
        # Проверка на уникальность имени пользователя
        if is_included(username_input):
            # Удаление сообщения от пользователя
            await message.delete()
            # Вывод сообщения о существовании пользователя
            reg_message = await message.answer(user_exist)
            reg_messages.append(reg_message.message_id)
            return
        # Проверка на корректность имени пользователя (только буквы латинского алфавита)
        if re.match("^[a-zA-Z]+$", username_input):
            await state.update_data(username=username_input)
            # Удаление сообщения от пользователя
            await message.delete()
            # Вывод сообщения о введенных данных
            bot_message = await message.answer(f'<b>Введенное имя пользователя: {username_input}</b>')
            user_info.append(bot_message.message_id)
            # Запрос на ввод email
            reg_message = await message.answer(email_input)
            reg_messages.append(reg_message.message_id)
            await state.set_state(RegistrationState.email)
        # Если имя пользователя не соответствует требованиям, вывод сообщения об ошибке
        else:
            # Если в процессе регистрации пользователь нажал любую кнопку меню,
            # процесс прерывается и выводится меню нажатой кнопки
            await repeat_reg.handle_menu_actions(message, state)
            # Удаление сообщения от пользователя с ошибкой ввода данных
            await message.delete()
            # Вывод сообщения об ошибке ввода данных
            reg_message = await message.answer(username_error)
            reg_messages.append(reg_message.message_id)


# Функция кнопки 'Регистрация'
# Получение значения электронной почты пользователя и добавление его в БД
@router.message(RegistrationState.email)
async def set_email(message: Message, state: FSMContext):
    with suppress(TelegramBadRequest):
        # Инициализация
        email_address = message.text
        # Проверка на корректность электронной почты
        if '@' in email_address or '.' in email_address:
            await state.update_data(email=email_address)
            # Удаление сообщения от пользователя
            await message.delete()
            # Вывод сообщения о введенных данных
            bot_message = await message.answer(f'<b>Введенный email: {email_address}</b>')
            user_info.append(bot_message.message_id)
            # Запрос на ввод возраста
            reg_message = await message.answer(age_input)
            reg_messages.append(reg_message.message_id)
            await state.set_state(RegistrationState.age)
        # Если электронная почта соответствует требованиям, вывод сообщения об ошибке
        else:
            # Если в процессе регистрации пользователь нажал любую кнопку меню,
            # процесс прерывается и выводится меню нажатой кнопки
            await repeat_reg.handle_menu_actions(message, state)
            # Удаление сообщения от пользователя с ошибкой ввода данных
            await message.delete()
            # Вывод сообщения об ошибке ввода данных
            reg_message = await message.answer(email_error)
            reg_messages.append(reg_message.message_id)


# Функция кнопки 'Регистрация'
# Получение значения возраста пользователя и добавление его в БД
@router.message(RegistrationState.age)
async def set_age_reg(message: Message, state: FSMContext):
    with suppress(TelegramBadRequest):
        # Инициализация
        user_age = message.text
        try:
            # Проверка на корректность возраста
            await state.update_data(age=int(user_age))
            # Удаление сообщения от пользователя
            await message.delete()
            # Вывод сообщения о введенных данных
            bot_message = await message.answer(f'<b>Введенный возраст: {user_age}</b>')
            user_info.append(bot_message.message_id)
            data = await state.get_data()
            # Добавление пользователя в БД
            add_user(data['username'], data['email'], data['age'])
            # Удаление всех сообщений от кнопки 'Регистрация'
            await reg_func.delete_all_reg_menu_messages(message)
            await menu_func.delete_menu_registration(message)
            # Вывод сообщения об успешной регистрации
            result = await message.answer(success_reg)
            reg_results.append(result.message_id)
            # Вывод информации о зарегистрированном пользователе
            result = await message.answer(f'<b>Имя пользователя:</b> {data["username"]}\n'
                                          f'<b>Email:</b> {data["email"]}\n'
                                          f'<b>Возраст:</b> {data["age"]}')
            reg_results.append(result.message_id)
            # Очистка данных машины состояния
            await state.clear()
        # Если возраст не является целым числом
        except ValueError:
            # Если в процессе регистрации пользователь нажал любую кнопку меню,
            # процесс прерывается и выводится меню нажатой кнопки
            await repeat_reg.handle_menu_actions(message, state)
            # Удаление сообщения от пользователя с ошибкой ввода данных
            await message.delete()
            # Вывод сообщения об ошибке ввода данных
            reg_message = await message.answer(age_error)
            reg_messages.append(reg_message.message_id)
