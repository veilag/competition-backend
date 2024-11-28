from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def handle_root():
    return {
        "message": "success"
    }
