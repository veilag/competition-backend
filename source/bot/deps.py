from aiogram.utils.web_app import check_webapp_signature, parse_webapp_init_data, WebAppInitData
from fastapi import Header, HTTPException, Query, WebSocketException, status
from typing import Annotated
from ..config import Config


async def authorize_user(x_telegram_auth: str = Annotated[str | None, Header()]) -> WebAppInitData:
    """
    Зависимость, которая проверяет запрос из Telegram мини-приложения
    """
    try:
        is_authorized = check_webapp_signature(Config.TELEGRAM_TOKEN, x_telegram_auth)

        if not is_authorized:
            raise HTTPException(status_code=403, detail="Данные WebApp невалидны")

        return parse_webapp_init_data(x_telegram_auth)

    except Exception:
        raise HTTPException(status_code=403, detail=f"Ошибка авторизации: {str(e)}")


async def authorize_user_connection(auth: Annotated[str | None, Query()] = None) -> WebAppInitData:
    """
    Зависимость, которая проверяет запрос из Telegram мини-приложения через WebSocket
    """
    try:
        is_authorized = check_webapp_signature(Config.TELEGRAM_TOKEN, auth)

        if not is_authorized:
            raise HTTPException(status_code=403, detail="Данные WebApp невалидны")

        return parse_webapp_init_data(auth)

    except Exception:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
