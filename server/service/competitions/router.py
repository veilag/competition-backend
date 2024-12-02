from typing import Dict
from sqlalchemy.exc import IntegrityError
from ...sockets.service import StandData
from aiogram.utils.web_app import WebAppInitData
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket
from ...sockets import SocketRouter
from .crud import create_competition, change_competitions_state, get_state, get_all_state
from ..users.crud import get_user_by_telegram_id
from .schemas import CompetitionCreate, StateModel

router = SocketRouter()


@router.on("COMPETITIONS:CREATE")
async def competition_create(
    event: str,
    data: Dict,
    session: AsyncSession,
    websocket: WebSocket,
    connections: Dict[WebSocket, WebAppInitData],
    stand_connections: Dict[WebSocket, StandData]
):
    user = await get_user_by_telegram_id(session, connections[websocket].user.id)

    if user.role.name == "admin":
        try:
            await create_competition(session, CompetitionCreate(**data))
        except IntegrityError as e:
            await websocket.send_json({
                "event": "COMPETITIONS:CREATE:RESULT",
                "status": "error",
                "data": {
                    "message": f"Ошибка: {e}"
                }
            })
            return

        await websocket.send_json({
                "event": "COMPETITIONS:CREATE:RESULT",
                "status": "success",
                "data": {
                    "message": f"Компетенция успешно создана"
                }
            })
        return

    await websocket.send_json({
        "event": "COMPETITIONS:CREATE:RESULT",
        "status": "error",
        "data": {
            "message": f"Вы не являетесь администратором"
        }
    })


@router.on("COMPETITIONS:GET_STATES")
async def competition_get_state(
    event: str,
    data: Dict,
    session: AsyncSession,
    websocket: WebSocket,
    connections: Dict[WebSocket, WebAppInitData],
    stand_connections: Dict[WebSocket, StandData]
):
    states = await get_all_state(session)
    await websocket.send_json({
        "event": "COMPETITIONS:GET_STATES",
        "status": "success",
        "data": [StateModel.from_orm(state).dict() for state in states]
    })


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
