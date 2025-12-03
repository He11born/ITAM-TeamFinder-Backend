from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# 1. Создание Engine (подключение к БД)
# pool_pre_ping=True - проверяет, живо ли соединение перед использованием
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL, 
    pool_pre_ping=True
)

# 2. Создание SessionLocal
# Это класс, который мы будем использовать для создания сессии в каждом запросе
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

# 3. Базовый класс для моделей
# Все наши модели БД будут наследоваться от этого класса
Base = declarative_base()

# --- Вспомогательная функция для Dependency Injection ---
# Эта функция будет использоваться в роутах FastAPI для получения сессии
def get_db():
    """
    Создает новую сессию БД для каждого запроса (Request)
    и закрывает ее после завершения (Response).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
