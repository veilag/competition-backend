from fastapi import APIRouter
from fastapi.responses import FileResponse, HTMLResponse

router = APIRouter(
    prefix="/templates",
    tags=["⚙️ Тестовые шаблоны"]
)


@router.get(
    path="/app",
    response_class=HTMLResponse,
    summary="Шаблон мини-приложения",
    description="Шаблон мини-приложения для тестирования, не используется в продакшене"
)
async def handle_app():
    return FileResponse('templates/app.html')


@router.get(
    path="/client"
)
async def handle_client():
    return FileResponse('templates/client.html')