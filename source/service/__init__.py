from .templates.router import router as templates_router
from .users.router import router as user_router
from .events.router import router as event_socket_router
from .competitions.router import router as competition_router

__all__ = [
    "templates_router",
    "user_router",
    "competition_router",
    "event_socket_router",
]
