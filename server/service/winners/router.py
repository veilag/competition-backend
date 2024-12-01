from typing import Dict
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket
from aiogram.utils.web_app import WebAppInitData
from ...sockets.service import StandData
from ...sockets import SocketRouter
from .crud import get_revealed_winners_by_competition
from .schemas import WinnerModel

router = SocketRouter()


@router.on("WINNERS:GET_REVEALED")
async def revealed_winners_by_competition(
    event: str,
    data: Dict,
    session: AsyncSession,
    websocket: WebSocket,
    connections: Dict[WebSocket, WebAppInitData],
    stand_connections: Dict[WebSocket, StandData]
):
    winners = await get_revealed_winners_by_competition(session, data.get("competition_id"))
    await websocket.send_json({
        "event": "WINNERS:GET_REVEALED",
        "status": "success",
        "data": {
            "winners": [WinnerModel.from_orm(winner).dict() for winner in winners]
        }
    })


@router.on("WINNERS:REVEAL")
async def reveal_winner(
    event: str,
    data: Dict,
    session: AsyncSession,
    websocket: WebSocket,
    connections: Dict[WebSocket, WebAppInitData],
    stand_connections: Dict[WebSocket, StandData]
):
    data.get("place", "competition_id")
    winners = await get_revealed_winners_by_competition(session, data.get("competition_id"))

    await websocket.send_json({
        "event": "WINNERS:GET_REVEALED",
        "status": "success",
        "data": {
            "winners": [WinnerModel.from_orm(winner).dict() for winner in winners]
        }
    })
