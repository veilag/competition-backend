from typing import Sequence
from sqlalchemy import select
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
