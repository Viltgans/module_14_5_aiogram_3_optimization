# Импорт необходимых модулей
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
from aiogram import Router, F
from aiogram.types import FSInputFile, CallbackQuery, Message
# Импорт листа из файла handlers/Messages.py
from ..handlers import Messages
# Импорт нужного текста из файла interface/text.py
from ..interface.text import buy_list, choose_product, success_buy
# Импорт клавиатуры с кнопками из файла interface/button.py
from ..interface.button import buy_menu
# Импорт функций для работы с базой данных
from ..database.data_product import *
from ..database.data_user import *

# Инициализация роутера
router = Router()

# Инициализация базы данных
initiate_product_db()
initiate_user_db()
products = get_all_products()

buy_messages = []
buy_results = []


# Функция для получения списка товаров для покупки
async def get_buying_list(message: Message):
    with suppress(TelegramBadRequest):
        buy_message = await message.answer(buy_list)
        Messages.menu_buy.append(buy_message.message_id)
        # Получение списка товаров из базы данных
        for product in products:
            id_, title, description, price = product
            photo = FSInputFile(f'files/Product{id_}.png', 'rb')
            bot_message = await message.answer_photo(photo,
                                                     caption=f'Название: {title}\nОписание: {description}\nЦена: {price}',
                                                     show_caption_above_media=True)
            buy_messages.append(bot_message.message_id)
        # Отправка кнопок для выбора товаров
        buy_message = await message.answer(choose_product, reply_markup=buy_menu)
        Messages.menu_buy.append(buy_message.message_id)


@router.callback_query(F.data.startswith('product_buying_'))
async def send_confirm_message(callback: CallbackQuery):
    with suppress(TelegramBadRequest):
        # Получение текста кнопки, соответствующий данным callback
        button_text = ''
        for row in callback.message.reply_markup.inline_keyboard:
            for button in row:
                if button.callback_data == callback.data:
                    button_text = button.text
        # Получение id продукта, соответствующего данной кнопке
        bot_message = await callback.bot.send_message(callback.from_user.id, success_buy + f'{button_text}!')
        buy_results.append(bot_message.message_id)
        await callback.answer()
