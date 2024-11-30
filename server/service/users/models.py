from ...database import Base
from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class User(Base):
    """
    Пользователь
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    public_id = Column(String, unique=True, nullable=False)
    telegram_id = Column(BigInteger, unique=True, nullable=False)

    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)

    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    in_place = Column(Boolean, nullable=False, default=False)
    approved = Column(Boolean, nullable=False, default=False)
    competition_id = Column(Integer, ForeignKey('competitions.id'), nullable=True)

    role = relationship("Role", back_populates="users")
    competition = relationship("Competition", back_populates="users")


class Role(Base):
    """
    Роль пользователя

    Возможные варианты
    - participant
    - mentor
    - judge
    - presenter
    - admin
    """
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    title = Column(String, unique=True, nullable=False)
    users = relationship("User", back_populates="role")
