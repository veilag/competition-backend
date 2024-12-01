from typing import Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Competition, CompetitionState
from .schemas import CompetitionCreate


async def create_competition(session: AsyncSession, competition_data: CompetitionCreate):
    session.add(Competition(**competition_data.dict()))
    await session.commit()


async def change_competitions_state(session: AsyncSession, state_id: int):
    await session.execute(
        update(Competition)
        .values({"state_id": state_id})
    )
    await session.commit()


async def get_state(session: AsyncSession, state_id: int) -> CompetitionState:
    query = await session.execute(
        select(CompetitionState)
        .where(CompetitionState.id == state_id)
    )

    return query.scalars().one()


async def get_all_state(session: AsyncSession) -> Sequence[CompetitionState]:
    query = await session.execute(
        select(CompetitionState)
    )

    return query.scalars().all()


async def init_states(session: AsyncSession) -> None:
    session.add_all([
        CompetitionState(
            id=1,
            name="Старт",
            type="start"
        ),
        CompetitionState(
            id=2,
            name="Регистрация",
            type="registration"
        ),
        CompetitionState(
            id=3,
            name="Выполнение заданий",
            type="task_solving"
        ),
        CompetitionState(
            id=4,
            name="Проверка заданий",
            type="checking"
        ),
        CompetitionState(
            id=5,
            name="Награждение",
            type="awarding"
        ),
        CompetitionState(
            id=6,
            name="Завтрак",
            type="breakfast"
        ),
        CompetitionState(
            id=7,
            name="Обед",
            type="lunch"
        ),
        CompetitionState(
            id=8,
            name="Ужин",
            type="dinner"
        ),
        CompetitionState(
            id=9,
            name="Завершено",
            type="end"
        ),
    ])

    await session.commit()
