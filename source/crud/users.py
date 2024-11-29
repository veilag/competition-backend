from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import User
from ..schemas.users import UserCreate


async def get_user_by_telegram_id(session: AsyncSession, telegram_id: int) -> User | None:
    query = await session.execute(
        select(User)
        .where(User.telegram_id == telegram_id)
    )

    return query.one_or_none()


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    query = await session.execute(
        select(User)
        .where(User.id == user_id)
    )

    return await query.one_or_none()


async def create_user(
    session: AsyncSession,
    user_data: UserCreate
):
    session.add(
        User(
            telegram_id=user_data.telegram_id,
            name=user_data.name,
            surname=user_data.surname,
            role=user_data.role,
            mentor_id=user_data.mentor_id,
            competition_id=user_data.competition_id
        )
    )

    await session.commit()
