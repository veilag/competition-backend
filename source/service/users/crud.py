from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from .utils import generate_public_id
from .models import User
from .schemas import UserCreate


async def get_user_by_telegram_id(session: AsyncSession, telegram_id: int) -> User | None:
    result = await session.execute(
        select(User)
        .options(joinedload(User.role), joinedload(User.competition))
        .where(User.telegram_id == telegram_id)
    )

    return result.scalars().one_or_none()


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    result = await session.execute(
        select(User)
        .where(User.id == user_id)
    )

    return result.scalars().one_or_none()


async def create_user(
    session: AsyncSession,
    user_data: UserCreate
):
    session.add(
        User(
            public_id=generate_public_id(),
            telegram_id=user_data.telegram_id,
            name=user_data.name,
            surname=user_data.surname,
            role_id=user_data.role_id,
        )
    )

    await session.commit()


async def get_users_in_place(session: AsyncSession) -> Sequence[User]:
    result = await session.execute(
        select(User)
        .options(joinedload(User.role), joinedload(User.competition))
        .where(User.in_place)
    )

    return result.scalars().all()
