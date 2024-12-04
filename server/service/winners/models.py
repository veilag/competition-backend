from sqlalchemy.orm import relationship
from ...database import Base
from sqlalchemy import Column, Integer, ForeignKey, Boolean, String


class Winner(Base):
    __tablename__ = 'winners'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    competition_id = Column(Integer, ForeignKey('competitions.id'), nullable=False)
    place = Column(Integer, nullable=False)
    revealed = Column(Boolean, nullable=False, default=False)

    user = relationship("User")


class NominationWinner(Base):
    __tablename__ = 'nomination_winners'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    competition_id = Column(Integer, ForeignKey('competitions.id'), nullable=False)

    name = Column(String, nullable=False)
    revealed = Column(Boolean, nullable=False, default=False)

    user = relationship("User")
