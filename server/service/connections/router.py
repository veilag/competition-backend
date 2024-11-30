from typing import Dict, Tuple
from aiogram.utils.web_app import WebAppInitData
from sqlalchemy.ext.asyncio import AsyncSession

from ..users.models import User
from .payloads import StateChangePayload, NewUserInPlacePayload
from ...sockets import StandData
from .constants import Event
from server.sockets import SocketRouter
from fastapi import WebSocket

router = SocketRouter()


@router.on(Event.COMPETITIONS_STATE_CHANGE)
async def competition_change(
    event: str,
    data: StateChangePayload,
    session: AsyncSession,
    websocket: WebSocket,
    connections: Dict[WebSocket, Tuple[WebAppInitData, User | None]],
    stand_connections: Dict[WebSocket, StandData]
):
    for stand_connection in stand_connections:
        await stand_connection.send_json({
            "event": Event.COMPETITIONS_STATE_CHANGE,
            "data": {
                "state": data["state"]
            }
        })
