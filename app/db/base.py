# app/db/base.py

from app.db.session import Base

# Импортируем все модели, чтобы Alembic их "увидел"
from app.db.models.user import User, Profile
from app.db.models.hackathon import Hackathon 
from app.db.models.team import Team, TeamMember, Invitation # <-- НОВЫЕ МОДЕЛИ
