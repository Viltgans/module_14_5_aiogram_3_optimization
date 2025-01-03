from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

keyboard = [
    [KeyboardButton(text='Рассчитать'),
     KeyboardButton(text='Информация')],
    [KeyboardButton(text='Купить'),
     KeyboardButton(text='Регистрация')]
]
kb = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)

inline_keyboard = [
    [
        InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories'),
        InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
    ]
]
inline_kb = InlineKeyboardMarkup(inline_keyboard=inline_keyboard, resize_keyboard=True)

buy_menu_keyboard = [
    [
        InlineKeyboardButton(text='Продукт 1', callback_data='product_buying_1'),
        InlineKeyboardButton(text='Продукт 2', callback_data='product_buying_2'),
        InlineKeyboardButton(text='Продукт 3', callback_data='product_buying_3'),
        InlineKeyboardButton(text='Продукт 4', callback_data='product_buying_4')
    ]
]
buy_menu = InlineKeyboardMarkup(inline_keyboard=buy_menu_keyboard, resize_keyboard=True)

inline_keyboard = [
    [
        InlineKeyboardButton(text='Мужской', callback_data='for_man'),
        InlineKeyboardButton(text='Женский', callback_data='for_woman')
    ]
]
formulas_kb = InlineKeyboardMarkup(inline_keyboard=inline_keyboard, resize_keyboard=True)

inline_keyboard = [
    [
        InlineKeyboardButton(text='Мужской', callback_data='man'),
        InlineKeyboardButton(text='Женский', callback_data='woman')
    ]
]
gender_kb = InlineKeyboardMarkup(inline_keyboard=inline_keyboard, resize_keyboard=True)
