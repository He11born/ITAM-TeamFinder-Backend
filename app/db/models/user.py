# app/db/models/user.py

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB # Идеально для массивов и словарей в PostgreSQL
from app.db.session import Base

# 1. Модель User (Данные авторизации)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True, nullable=False) # ID, полученный при авторизации
    
    # Данные из Telegram
    username = Column(String, index=True, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    
    # Системные флаги для Организатора
    is_active = Column(Boolean, default=True)
    is_organizer = Column(Boolean, default=False) 

    # --- Связи (Relationships) ---
    # Профиль (1:1)
    profile = relationship("Profile", back_populates="owner", uselist=False)
    
    # Команды, где пользователь — капитан (1:M)
    teams_owned = relationship("Team", back_populates="captain") 
    
    # Членство в командах (M:M через TeamMember)
    team_memberships = relationship("TeamMember", back_populates="user")


# 2. Модель Profile (Анкета участника)
class Profile(Base):
    __tablename__ = "profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Внешний ключ: Связь с User (1:1)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Анкетные данные
    bio = Column(String, nullable=True)
    desired_role = Column(String, nullable=True) # Например: 'Backend', 'Designer', 'Product Manager'
    experience = Column(String, nullable=True) # Например: 'Junior', 'Middle', 'Senior'

    # Навыки: JSONB позволяет хранить массив строк (['Python', 'FastAPI', 'PostgreSQL'])
    # Это ключевой элемент для "Быстрый поиск сокомандников с фильтрами по технологиям".
    skills = Column(JSONB, default=[]) 
    
    # Флаг для "Анкета пользователя видна для потенциальных команд"
    is_visible = Column(Boolean, default=True)

    # Обратная связь к User
    owner = relationship("User", back_populates="profile")
