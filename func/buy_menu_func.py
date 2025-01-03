# Импорт необходимых модулей
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

# Импорт листов из файла handlers/Buying.py
from ..handlers import Buying


# Функция для удаления всех сообщений, которые были отправлены в чат
# во время инициализации кнопки меню "Купить" и самого меню покупки
async def delete_all_buy_menu_messages(message: Message):
    with suppress(TelegramBadRequest):
        chat_id = message.chat.id

        for msg_id in Buying.buy_messages[::-1]:
            try:
                await message.bot.delete_message(chat_id=chat_id, message_id=msg_id)
            except Exception as e:
                print(f"Ошибка: {e}")
        Buying.buy_messages.clear()

        for msg_id in Buying.buy_results[::-1]:
            try:
                await message.bot.delete_message(chat_id=chat_id, message_id=msg_id)
            except Exception as e:
                print(f"Ошибка: {e}")
        Buying.buy_results.clear()
