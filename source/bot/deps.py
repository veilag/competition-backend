from aiogram.utils.web_app import safe_parse_webapp_init_data, WebAppInitData
from fastapi import Header, HTTPException, Query, WebSocketException, status, Depends
from typing import Annotated, List
from sqlalchemy.ext.asyncio import AsyncSession
from ..config import Config
from ..crud import get_user_by_telegram_id
from ..database import get_db
from ..models import User


async def authorize_user(
    x_telegram_auth: Annotated[str | None, Header()] = None,
    session: AsyncSession = Depends(get_db)
) -> List[WebAppInitData | User | None]:
    """
    Зависимость, которая проверяет запрос из Telegram мини-приложения
    """
    try:
        user_telegram_data = safe_parse_webapp_init_data(
            token=Config.TELEGRAM_TOKEN,
            init_data=x_telegram_auth
        )

        user = await get_user_by_telegram_id(session, user_telegram_data.user.id)
        return [user_telegram_data, user]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Невалидная сигнатура WebApp данных"
        )


async def authorize_user_connection(
    token: Annotated[str | None, Query()] = None,
    session: AsyncSession = Depends(get_db)
) -> List[WebAppInitData | User | None]:
    """
    Зависимость, которая проверяет запрос из Telegram мини-приложения через WebSocket
    """
    try:
        user_telegram_data = safe_parse_webapp_init_data(Config.TELEGRAM_TOKEN, token)
        user = await get_user_by_telegram_id(session, user_telegram_data.user.id)

        return [user_telegram_data, user]

    except Exception:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
