# Импортируем базовый класс для всех моделей
from app.db.session import Base

# Импортируем все модели, чтобы Alembic их "увидел"
from app.db.models.user import User  # Пока этих файлов нет, мы их создадим далее
from app.db.models.hackathon import Hackathon 
from app.db.models.team import Team
# ... и другие
