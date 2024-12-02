from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from .utils import generate_public_id
from .models import User, Role
from .schemas import UserCreate
from ..competitions.models import Competition


async def get_user_by_telegram_id(session: AsyncSession, telegram_id: int) -> User | None:
    result = await session.execute(
        select(User)
        .options(
            joinedload(User.role),
            joinedload(User.competition)
            .joinedload(Competition.state)
        )
        .where(User.telegram_id == telegram_id)
    )

    return result.scalars().one_or_none()


async def get_user_by_public_id(session: AsyncSession, public_id: int) -> User | None:
    result = await session.execute(
        select(User)
        .options(
            joinedload(User.role),
            joinedload(User.competition)
            .joinedload(Competition.state)
        )
        .where(User.public_id == public_id)
    )

    return result.scalars().one_or_none()


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    result = await session.execute(
        select(User)
        .options(
            joinedload(User.role),
            joinedload(User.competition)
            .joinedload(Competition.state)
        )
        .where(User.id == user_id)
    )

    return result.scalars().one_or_none()


async def create_user(
    session: AsyncSession,
    user_data: UserCreate
):
    user = User(**user_data.dict())
    user.public_id = generate_public_id()
    session.add(user)
    await session.commit()


async def get_users_in_place(session: AsyncSession) -> Sequence[User]:
    result = await session.execute(
        select(User)
        .options(joinedload(User.role), joinedload(User.competition))
        .where(User.in_place)
    )

    return result.scalars().all()


async def get_user_count(session: AsyncSession) -> int:
    result = await session.execute(
        select(User)
        .with_only_columns(User.id)
    )

    return len(result.all())


async def init_roles(session: AsyncSession) -> None:
    session.add_all([
        Role(
            id=1,
            name='Администратор',
            type='admin'
        ),
        Role(
            id=2,
            name='Участник',
            type='participant'
        ),
        Role(
            id=3,
            name='Наставник',
            type='mentor'
        ),
        Role(
            id=4,
            name='Жюри',
            type='judge'
        ),
        Role(
            id=5,
            name='Управляющий',
            type='staff'
        ),
    ])

    await session.commit()
