from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

# Базовый класс для настроек приложения
class Settings(BaseSettings):
    # Указываем, откуда брать переменные окружения
    # .env.local - файл будет искаться автоматически
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"  # Игнорировать переменные, которые не объявлены в классе
    )

    # --- Общие Настройки Проекта ---
    PROJECT_NAME: str = "ITAM Team Finder API"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str  # Будет использоваться для JWT-токенов
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 дней

    # --- Настройки Telegram Авторизации ---
    # Токен вашего Telegram-бота, который используется для проверки подписи
    TELEGRAM_BOT_TOKEN: str
    
    # --- Настройки PostgreSQL ---
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str = "5432"

    # Свойство для формирования URL подключения к БД
    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        # Пример: postgresql://user:password@server:port/db_name
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # --- Настройки Redis ---
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379


settings = Settings()
