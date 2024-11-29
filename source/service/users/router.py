from typing import List
from aiogram.utils.web_app import WebAppInitData
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..auth.deps import authorize_user, authorize_stand
from ...database import get_db
from .models import User
from .schemas import UserModel, UserCreate
from .crud import create_user, get_users_in_place
from ..schemas import MessageResponse

router = APIRouter(
    prefix="/users",
)


@router.get(
    path="/me",
    response_model=UserModel,
    tags=["👤 Пользователи"],
    summary="Данные пользователя",
    description="Получение данных пользователя мини-приложения"
)
async def send_user_credentials(
    auth_data: List[WebAppInitData | User | None] = Depends(authorize_user),
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

    return UserModel.from_orm(user)


@router.post(
    path="/register",
    response_model=MessageResponse,
    tags=["📝 Регистрация"],
    summary="Регистрация пользователя",
    description="Регистрация пользователя через мини-приложение"
)
async def register_user(
    user_data: UserCreate,
    auth_data: List[WebAppInitData | User | None] = Depends(authorize_user),
    session: AsyncSession = Depends(get_db),
):
    """
    Регистрация пользователя через мини-приложение
    """
    _, user = auth_data

    if not user:
        await create_user(session, user_data)
        return {
            "message": "Пользователь успешно зарегистрирован"
        }

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Пользователь уже зарегистрирован"
        )


@router.get(
    path="/all",
    tags=["👤 Пользователи"],
    summary="Пользователи, которые прошли проверку на входе",
    description="Возвращает список пользователей, прошедших сканирование QR-кода"
)
async def users_in_place(
    session: AsyncSession = Depends(get_db),
    _=Depends(authorize_stand)
):
    """
    Все пользователи, которые прошли проверку на входе
    Доступно только из стендов
    """
    users = await get_users_in_place(session)
    return [UserModel.from_orm(user) for user in users]
