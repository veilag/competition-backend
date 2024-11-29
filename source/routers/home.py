from fastapi import APIRouter
from starlette.responses import FileResponse

router = APIRouter(tags=["⚙️ Разное"])


@router.get("/")
async def handle_root():
    return {
        "message": "success"
    }


@router.get("/app")
async def handle_app():
    return FileResponse('templates/app.html')
