from fastapi import APIRouter

router = APIRouter(
    prefix="/competitions",
    tags=["📚 Компетенции (Олимпиады)"]
)


@router.get(
    path="",
    summary="Все компетенции",
    description="Список всех созданных компетенций"
)
async def all_competitions():
    ...


@router.get(
    path="/{competition_id}",
    summary="Компетенция",
    description="Компетенция по выбранному ID"
)
async def competition_by_id():
    ...

