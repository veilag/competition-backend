from ...database import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship


class Competition(Base):
    """
    Олимпиада
    """
    __tablename__ = 'competitions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    state_id = Column(Integer, ForeignKey('states.id'), nullable=True)

    state = relationship("CompetitionState", back_populates="competitions")
    users = relationship("User", back_populates="competition")


class CompetitionState(Base):
    """
    Состояние олимпиады

    Возможные варианты
    - registration
    - breakfast
    - dinner
    - lunch
    - in_process
    - checking
    - awarding
    """
    __tablename__ = 'states'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    competitions = relationship("Competition", back_populates="state")
