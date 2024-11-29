from typing import Dict
from aiogram.utils.web_app import WebAppInitData
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
    websocket: WebSocket,
    connections: Dict[WebSocket, WebAppInitData],
    stand_connections: Dict[WebSocket, StandData]
):
    for stand_connection in stand_connections:
        await stand_connection.send_json({
            "event": Event.COMPETITIONS_STATE_CHANGE,
            "data": {
                "state": data["state"]
            }
        })


@router.on(Event.NEW_USER_IN_PLACE)
async def user_in_place(
    event: str,
    data: NewUserInPlacePayload,
    websocket: WebSocket,
    connections: Dict[WebSocket, WebAppInitData],
    stand_connections: Dict[WebSocket, StandData]
):
    for stand_connection in stand_connections:
        if stand_connections[stand_connection]["type"] != "registration":
            continue

        await stand_connection.send_json({
            "event": Event.NEW_USER_IN_PLACE,
            "data": data
        })
