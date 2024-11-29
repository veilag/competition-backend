from typing import Annotated
from fastapi import Query, WebSocketException, status
from ..config import Config


async def authorize_stand(
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
