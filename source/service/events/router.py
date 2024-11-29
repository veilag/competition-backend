from typing import Dict
from aiogram.utils.web_app import WebAppInitData
from ...sockets import StandData
from source.sockets import SocketRouter
from fastapi import WebSocket

router = SocketRouter()


@router.on("MESSAGE")
async def handle_message(
    event: str,
    data: Dict,
    websocket: WebSocket,
    connections: Dict[WebSocket, WebAppInitData],
    stand_connections: Dict[WebSocket, StandData]
):
    await websocket.send_json({
        "message": data["message"]
    })
