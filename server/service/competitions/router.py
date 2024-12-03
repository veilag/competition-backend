from typing import Dict
from ...sockets.service import StandData
from aiogram.utils.web_app import WebAppInitData
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket
from ...sockets import SocketRouter
from .crud import change_competitions_state, get_state, get_current_state
from ..users.crud import get_user_by_telegram_id
from .schemas import StateModel

router = SocketRouter()


@router.on("COMPETITIONS:CHANGE_STATE")
async def competition_change(
    event: str,
    data: Dict,
    session: AsyncSession,
    websocket: WebSocket,
    connections: Dict[WebSocket, WebAppInitData],
    stand_connections: Dict[WebSocket, StandData]
):
    user = await get_user_by_telegram_id(session, connections[websocket].user.id)
    if user.role.type == "admin":
        state = await get_state(session, data.get("state_id"))
        await change_competitions_state(session, data.get("state_id"))

        await websocket.send_json({
            "event": "COMPETITIONS:CHANGE_STATE:RESULT",
            "status": "success",
            "data": {
                "message": "Статус был успешно изменен"
            }
        })

        for connection in connections:
            await connection.send_json({
                "event": "COMPETITIONS:STATE_CHANGE",
                "data": {
                    "state": StateModel.from_orm(state).dict()
                }
            })

        for connection in stand_connections:
            await connection.send_json({
                "event": "COMPETITIONS:STATE_CHANGE",
                "data": {
                    "state": StateModel.from_orm(state).dict()
                }
            })


@router.on("COMPETITIONS:GET_STATE")
async def competition_state(
    event: str,
    data: Dict,
    session: AsyncSession,
    websocket: WebSocket,
    connections: Dict[WebSocket, WebAppInitData],
    stand_connections: Dict[WebSocket, StandData]
):
    state = await get_current_state(session)

    await websocket.send_json({
        "event": "COMPETITIONS:GET_STATE",
        "data": {
            "state": StateModel.from_orm(state).dict()
        }
    })
