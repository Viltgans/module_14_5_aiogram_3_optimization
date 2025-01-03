# Импорт необходимых модулей
from contextlib import suppress
from aiogram import html, Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

# Импорт модулей с функциями из папки func, чтобы избавиться от дублирования кода
from ..func import repeat_calc
# Импорт клавиатуры с кнопками из файла interface/button.py
from ..interface.button import gender_kb, formulas_kb
# Импорт нужного текста из файла interface/text.py
from ..interface.text import *
# Импорт функций из файла func/calculator_func.py
from ..func import calculator_func

# Инициализация списков для хранения сообщений
messages = []
messages_man = []
messages_woman = []
messages_input = []
formulas = []
calories = []
results = []

# Инициализация роутера
router = Router()


# Инициализация машины состояний для пользователя
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()


# Общая функция для добавления сообщений в списки
async def add_message_to_lists(message_id, lists):
    for lst in lists:
        lst.append(message_id)


# Функция для inline-кнопки 'Формулы расчёта'
@router.callback_query(F.data == 'formulas')
async def get_formulas(callback: CallbackQuery):
    with suppress(TelegramBadRequest):
        # Инициализация
        bot_message = await callback.message.answer(gender_input, reply_markup=formulas_kb)
        await add_message_to_lists(bot_message.message_id, [formulas])
        # Логика удаления сообщений
        if len(calories) > 0:
            await calculator_func.delete_calories(callback)
        if len(messages_woman) > 0:
            await calculator_func.delete_woman_messages(callback)
        if len(messages_man) > 0:
            await calculator_func.delete_man_messages(callback)
        if len(results) > 0:
            await calculator_func.delete_result_messages(callback)


# Функция для inline-кнопки 'Рассчитать норму калорий'
@router.callback_query(F.data == 'calories')
async def set_gender(callback: CallbackQuery, state: FSMContext):
    with suppress(TelegramBadRequest):
        # Инициализация
        await state.set_state(UserState.gender)
        bot_message = await callback.message.answer(gender_input, reply_markup=gender_kb)
        await add_message_to_lists(bot_message.message_id, [calories])
        # Логика удаления сообщений
        if len(formulas) > 0:
            await calculator_func.delete_formulas(callback)
        if len(messages_woman) > 0:
            await calculator_func.delete_woman_messages(callback)
        if len(messages_man) > 0:
            await calculator_func.delete_man_messages(callback)
        await callback.answer()


# Функция в подменю inline-кнопки 'Формулы расчёта' для inline-кнопки 'Мужской'
@router.callback_query(F.data == 'for_man')
async def get_formulas(callback: CallbackQuery):
    with suppress(TelegramBadRequest):
        # Инициализация
        bot_message = await callback.message.answer(formula_for_man)
        await add_message_to_lists(bot_message.message_id, [messages_man])
        # Логика удаления сообщений
        if len(messages_woman) > 0:
            await calculator_func.delete_woman_messages(callback)
        await callback.answer()


# Функция в подменю inline-кнопки 'Формулы расчёта' для inline-кнопки 'Женский'
@router.callback_query(F.data == 'for_woman')
async def get_formulas(callback: CallbackQuery):
    with suppress(TelegramBadRequest):
        # Инициализация
        bot_message = await callback.message.answer(formula_for_woman)
        await add_message_to_lists(bot_message.message_id, [messages_woman])
        # Логика удаления сообщений
        if len(messages_man) > 0:
            await calculator_func.delete_man_messages(callback)
        await callback.answer()


# Функция в подменю inline-кнопки 'Рассчитать норму калорий' для inline-кнопки 'Мужской'
@router.callback_query(F.data == 'man')
async def calc_for_man(callback: CallbackQuery, state: FSMContext):
    with suppress(TelegramBadRequest):
        # Инициализация
        await set_age(callback, state)
        # Логика удаления сообщений
        if len(results) > 0:
            await calculator_func.delete_result_messages(callback)
        if len(messages_woman) > 0:
            await calculator_func.delete_woman_messages(callback)
        await callback.answer()


# Функция в подменю inline-кнопки 'Рассчитать норму калорий' для inline-кнопки 'Женский'
@router.callback_query(F.data == 'woman')
async def calc_for_woman(callback: CallbackQuery, state: FSMContext):
    with suppress(TelegramBadRequest):
        # Инициализация
        await set_age(callback, state)
        # Логика удаления сообщений
        if len(results) > 0:
            await calculator_func.delete_result_messages(callback)
        if len(messages_man) > 0:
            await calculator_func.delete_man_messages(callback)
        await callback.answer()


# Функция расчета нормы калорий в подменю inline-кнопки 'Рассчитать норму калорий'
# Получение значения пола
@router.callback_query(UserState.gender)
async def set_age(callback: CallbackQuery, state: FSMContext):
    with suppress(TelegramBadRequest):
        # Инициализация
        await state.update_data(gender=callback.data)
        await state.set_state(UserState.age)
        data = await state.get_data()
        input_text = man_age_input if data['gender'] == 'man' else woman_age_input
        bot_message = await callback.message.answer(input_text)
        # добавляем в список messages для удаления при аргументе Message
        # и в messages_man и messages_woman при удалении при аргументе CallbackQuery
        await add_message_to_lists(bot_message.message_id,
                                   [messages, messages_man if data['gender'] == 'man' else messages_woman])
        messages.append(bot_message.message_id)
        await callback.answer()


# Функция расчета нормы калорий в подменю inline-кнопки 'Рассчитать норму калорий'
# Получение значения возраста
@router.message(UserState.age)
async def set_growth(message: Message, state: FSMContext):
    with suppress(TelegramBadRequest):
        user_message = message.text
        try:
            # Инициализация
            await state.update_data(age=int(user_message))
            # Удаление сообщения от пользователя
            await message.delete()
            # Вывод сообщения о введенных данных
            bot_message = await message.answer(f'<b>Введенный возраст: {user_message}</b>')
            # добавляем в список messages для удаления при аргументе Message
            # и в messages_input для удаления при аргументе CallbackQuery
            await add_message_to_lists(bot_message.message_id, [messages, messages_input])
            await state.set_state(UserState.growth)
            data = await state.get_data()
            #  для inline-кнопки 'Мужской'
            input_text = man_growth_input if data['gender'] == 'man' else woman_growth_input
            bot_message = await message.answer(input_text)
            await add_message_to_lists(bot_message.message_id,
                                       [messages, messages_man if data['gender'] == 'man' else messages_woman])
        # Обработка ошибок ввода данных и других reply-кнопок основного меню
        except ValueError:
            # Если в процессе регистрации пользователь нажал любую кнопку меню,
            # процесс прерывается и выводится меню нажатой кнопки
            await repeat_calc.handle_menu_actions(message, state)
            # Удаление сообщения от пользователя с ошибкой ввода данных
            await message.delete()
            # Вывод сообщения об ошибке ввода данных
            bot_message = await message.answer(age_error)
            messages.append(bot_message.message_id)


# Функция расчета нормы калорий в подменю inline-кнопки 'Рассчитать норму калорий'
# Получение значения роста
@router.message(UserState.growth)
async def set_weight(message: Message, state: FSMContext):
    with suppress(TelegramBadRequest):
        try:
            # Инициализация
            user_message = message.text
            await state.update_data(growth=int(user_message))
            # Удаление сообщения от пользователя
            await message.delete()
            # Вывод сообщения о введенных данных
            bot_message = await message.answer(f'<b>Введенный рост: {user_message}</b>')
            # добавляем в список messages для удаления при аргументе Message
            # и в messages_input для удаления при аргументе CallbackQuery
            await add_message_to_lists(bot_message.message_id, [messages, messages_input])
            await state.set_state(UserState.weight)
            data = await state.get_data()
            input_text = man_weight_input if data['gender'] == 'man' else woman_weight_input
            bot_message = await message.answer(input_text)
            await add_message_to_lists(bot_message.message_id,
                                       [messages, messages_man if data['gender'] == 'man' else messages_woman])
        # Обработка ошибок ввода данных и других reply-кнопок основного меню
        except ValueError:
            # Если в процессе регистрации пользователь нажал любую кнопку меню,
            # процесс прерывается и выводится меню нажатой кнопки
            await repeat_calc.handle_menu_actions(message, state)
            # Удаление сообщения от пользователя с ошибкой ввода данных
            await message.delete()
            # Вывод сообщения об ошибке ввода данных
            bot_message = await message.answer(growth_error)
            messages.append(bot_message.message_id)


# Функция расчета нормы калорий в подменю inline-кнопки 'Рассчитать норму калорий'
# Получение значения веса
@router.message(UserState.weight)
async def send_calories(message: Message, state: FSMContext):
    with suppress(TelegramBadRequest):
        try:
            user_message = message.text
            await state.update_data(weight=int(user_message))
            # Удаление сообщения от пользователя
            await message.delete()
            # Вывод сообщения о введенных данных
            bot_message = await message.answer(f'<b>Введенный вес: {user_message}</b>')
            # добавляем в список messages для удаления при аргументе Message
            # и в messages_input для удаления при аргументе CallbackQuery
            await add_message_to_lists(bot_message.message_id, [messages, messages_input])
            data = await state.get_data()
            await calculator_func.delete_all_menu_calc_and_formula(message)
            result = (10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) +
                      (5 if data['gender'] == 'man' else -161))
            bot_message = await message.answer(
                f'{html.bold(html.quote(message.from_user.full_name))}! '
                f'Ваша норма калорий <b>{result:.2f}</b>', parse_mode='HTML')
            results.append(bot_message.message_id)
            # Очистка данных машины состояний
            await state.clear()
        except ValueError:
            # Если в процессе регистрации пользователь нажал любую кнопку меню,
            # процесс прерывается и выводится меню нажатой кнопки
            await repeat_calc.handle_menu_actions(message, state)
            # Удаление сообщения от пользователя с ошибкой ввода данных
            await message.delete()
            # Вывод сообщения об ошибке ввода данных
            bot_message = await message.answer(weight_error)
            messages.append(bot_message.message_id)
