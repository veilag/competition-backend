from ..database import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship


class Competition(Base):
    """
    Олимпиада
    """
    __tablename__ = 'competitions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    state_id = Column(Integer, ForeignKey('states.id'), nullable=True)  # Текущее состояние

    state = relationship("State", back_populates="competitions")
    users = relationship("User", back_populates="competition")


class State(Base):
    """
    Состояние олимпиады

    Возможные варианты
    - registration
    - breakfast
    - dinner
    - lunch
    - to_offices
    - in_process
    - checking
    - awarding
    """
    __tablename__ = 'states'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    type = Column(String, nullable=False)
    competitions = relationship("Competition", back_populates="state")
