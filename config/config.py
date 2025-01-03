from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


# Класс настроек для хранения конфиденциальной информации токена бота
class Settings(BaseSettings):
    bot_token: SecretStr
    model_config = SettingsConfigDict(env_file='config/.env', env_file_encoding='utf-8')


config = Settings()
