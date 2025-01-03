# Импорт необходимых модулей
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

# Импорт листов из файла handlers/Registration.py
from ..handlers import Registration


# Функция для удаления всех сообщений, которые были отправлены в чат
# во время инициализации кнопки меню "Регистрация" и самой регистрации.
async def delete_all_reg_menu_messages(message: Message):
    with suppress(TelegramBadRequest):
        chat_id = message.chat.id

        # Общая функция для удаления сообщений из списка и его очистки
        async def delete_messages(message_list: list):
            for msg_id in message_list[::-1]:
                try:
                    await message.bot.delete_message(chat_id=chat_id, message_id=msg_id)
                except TelegramBadRequest as e:
                    print(f"Ошибка при удалении сообщения: {e}")
            message_list.clear()

    # Удаление сообщений из всех списков
    await delete_messages(Registration.reg_messages)
    await delete_messages(Registration.user_info)
    await delete_messages(Registration.reg_results)
