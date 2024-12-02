from typing import Sequence
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from ..winners.models import Winner
from ..users.models import User


async def get_revealed_winners_by_competition(session: AsyncSession, competition_id: int) -> Sequence[Winner]:
    query = await session.execute(
        select(Winner)
        .options(
            joinedload(Winner.user)
            .joinedload(User.competition)
        )
        .where(
            Winner.competition_id == competition_id,
            Winner.revealed
        )
    )

    return query.scalars().all()


async def create_winner(session: AsyncSession, competition_id: int, user_id: int, place: int) -> None:
    session.add(
        Winner(
            user_id=user_id,
            competition_id=competition_id,
            place=place,
            revealed=False
        )
    )

    await session.commit()


async def get_winners_by_competitions(session: AsyncSession, competition_id: int) -> Sequence[Winner]:
    query = await session.execute(
        select(Winner)
        .options(
            joinedload(Winner.user)
            .joinedload(User.competition)
        )
        .where(Winner.competition_id == competition_id)
    )

    return query.scalars().all()


async def update_winners_reveal_by_competition(session: AsyncSession, competition_id: int) -> None:
    await session.execute(
        update(Winner)
        .values({"revealed": True})
        .where(Winner.competition_id == competition_id)
    )

    await session.commit()
