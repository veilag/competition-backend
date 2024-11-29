from typing import Annotated
from aiogram.utils.web_app import WebAppInitData
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..bot import authorize_user
from ..database import get_db
from ..schemas.users import UserResponse, UserCreate
from ..crud import create_user

router = APIRouter(
    tags=["👤 Пользователи"]
)


@router.get(
    path="/me",
    response_model=UserResponse,
    summary="Данные пользователя",
    description="Получение данных пользователя мини-приложения"
)
async def send_user_credentials(
    auth_data: Annotated[WebAppInitData, Depends(authorize_user)],
):
    """
    Получение данных пользователя мини-приложения
    """
    _, user = auth_data
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не зарегистрирован на сервере"
        )

    return UserResponse.from_orm(user)


@router.post(
    path="/register",
    summary="Регистрация пользователя",
    description="Регистрация пользователя через мини-приложение"
)
async def register_user(
    user_data: UserCreate,
    _: Annotated[WebAppInitData, Depends(authorize_user)],
    session: AsyncSession = Depends(get_db),
):
    """
    Регистрация пользователя через мини-приложение
    """
    await create_user(session, user_data)
