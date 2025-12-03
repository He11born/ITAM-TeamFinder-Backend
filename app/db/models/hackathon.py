# app/db/models/hackathon.py

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from app.db.session import Base
from datetime import datetime

# Модель Hackathon (Событие)
class Hackathon(Base):
    __tablename__ = "hackathons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    
    # Даты проведения
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=False)
    
    # Статус (управляется организатором)
    is_active = Column(Boolean, default=True)
    
    # Параметры: JSONB для гибких настроек (например, макс. размер команды, разрешенные стеки)
    parameters = Column(JSONB, default={})
    
    # --- Связи ---
    # Команды, относящиеся к этому хакатону (1:M)
    teams = relationship("Team", back_populates="hackathon")
