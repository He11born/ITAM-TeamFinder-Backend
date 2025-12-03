# app/db/models/team.py

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint
from app.db.session import Base
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB

# 1. Модель Команды (Team)
class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    
    # Статус: открыт ли набор
    is_recruiting = Column(Boolean, default=True) 
    
    # Требуемые роли/навыки: JSONB для объявления, кого ищет команда
    required_skills = Column(JSONB, default=[])

    # --- Связи с другими моделями ---
    
    # Капитан: Внешний ключ на таблицу users.id
    captain_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    captain = relationship("User", back_populates="teams_owned") # Обратная связь в user.py
    
    # Хакатон: Внешний ключ на hackathons.id
    hackathon_id = Column(Integer, ForeignKey("hackathons.id"), nullable=False)
    hackathon = relationship("Hackathon", back_populates="teams") # Обратная связь в hackathon.py

    # Члены команды (1:M на TeamMember)
    members = relationship("TeamMember", back_populates="team", cascade="all, delete")
    
    # Приглашения, отправленные командой
    invitations_sent = relationship("Invitation", back_populates="team", cascade="all, delete")


# 2. Модель Членства (TeamMember)
# Служит для реализации связи "Многие-ко-Многим" между User и Team
class TeamMember(Base):
    __tablename__ = "team_members"
    
    # Уникальность: один пользователь может быть только один раз в одной команде
    __table_args__ = (
        UniqueConstraint('team_id', 'user_id', name='_team_user_uc'),
    )

    id = Column(Integer, primary_key=True, index=True)
    
    # Внешние ключи
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Роль пользователя в команде (например, "Lead Backend Developer")
    role_in_team = Column(String, nullable=True) 

    # Обратные связи
    team = relationship("Team", back_populates="members")
    user = relationship("User", back_populates="team_memberships")


# 3. Модель Приглашения (Invitation)
# Необходима для реализации функционала "Капитан команды может отправить приглашение пользователю"
class Invitation(Base):
    __tablename__ = "invitations"

    id = Column(Integer, primary_key=True, index=True)
    
    # ID отправителя (Команды) и получателя (Пользователя)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    recipient_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Текст сообщения/мотивации
    message = Column(String, nullable=True)
    
    # Статус: 'pending', 'accepted', 'rejected'
    status = Column(String, default="pending") 
    
    # Дата создания для истечения срока действия
    created_at = Column(DateTime, default=datetime.utcnow)

    # Обратные связи
    team = relationship("Team", back_populates="invitations_sent")
    # Обратная связь к получателю (будет в user.py, как "invitations_received")
