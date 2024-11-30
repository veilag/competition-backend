from aiogram.utils.web_app import safe_parse_webapp_init_data, WebAppInitData
from fastapi import Query, WebSocketException, status
from typing import Annotated
from ...config import Config


async def authorize_user_connection(
    token: Annotated[str | None, Query()] = None,
) -> WebAppInitData:
    """
    Зависимость, которая проверяет запрос из Telegram мини-приложения через WebSocket
    """
    try:
        user_telegram_data = safe_parse_webapp_init_data(Config.TELEGRAM_TOKEN, token)
        return user_telegram_data

    except Exception:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)


async def authorize_stand_connection(
    token: Annotated[str | None, Query()] = None,
    type: Annotated[str | None, Query()] = None,
    id: Annotated[str | None, Query()] = None
):
    if token != Config.STAND_TOKEN:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

    return {
        "type": type,
        "id": id
    }
