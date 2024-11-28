from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from sqlalchemy.future import select

from ..models import User

router = APIRouter()


@router.get("/")
async def handle_root(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    print(result.all())

    return {
        "message": "success"
    }
