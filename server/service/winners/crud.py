from typing import Sequence
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from ..winners.models import Winner, NominationWinner
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


async def create_nomination_winner(session: AsyncSession, competition_id: int, user_id: int, name: str) -> None:
    session.add(
        NominationWinner(
            user_id=user_id,
            competition_id=competition_id,
            name=name,
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


async def get_winner_by_place(session: AsyncSession, competition_id: int, place: int) -> Winner:
    query = await session.execute(
        select(Winner)
        .options(
            joinedload(Winner.user)
            .joinedload(User.competition)
        )
        .where(Winner.competition_id == competition_id, Winner.place == place)
    )

    return query.scalars().one()


async def get_nomination_winner(session: AsyncSession, competition_id: int, name: str) -> NominationWinner:
    query = await session.execute(
        select(NominationWinner)
        .options(
            joinedload(NominationWinner.user)
            .joinedload(User.competition)
        )
        .where(NominationWinner.competition_id == competition_id, NominationWinner.name == name)
    )

    return query.scalars().one()


async def update_winner_reveal_by_competition(session: AsyncSession, competition_id: int, place: int) -> None:
    await session.execute(
        update(Winner)
        .values({"revealed": True})
        .where(Winner.competition_id == competition_id, Winner.place == place)
    )

    await session.commit()


async def update_nomination_winner_reveal_by_competition(session: AsyncSession, competition_id: int, name: str) -> None:
    await session.execute(
        update(NominationWinner)
        .values({"revealed": True})
        .where(NominationWinner.competition_id == competition_id, NominationWinner.name == name)
    )

    await session.commit()
