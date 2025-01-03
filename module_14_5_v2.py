# Импорт необходимых модулей
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

# Импорт хэндлеров
from module_14.homework_14_5_v2.handlers import Messages, Registration, Buying, Calculator
# Импорт конфига
from module_14.homework_14_5_v2.config.config import config

# Инициализация бота с токеном из конфига и стандартными параметрами для aiogram
bot = Bot(token=config.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode='HTML'))


async def main():
    # Инициализация диспетчера
    dp = Dispatcher(storage=MemoryStorage())

    # Подключение хэндлеров
    routers = [Calculator.router, Buying.router, Registration.router, Messages.router]
    dp.include_routers(*routers)

    # Запуск поллинга с удалением вебхука
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    # Запуск бота
    asyncio.run(main())
