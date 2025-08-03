from typing import Any, Dict

from fastapi import APIRouter

from app.api.routers import auth, user

NOT_FOUND_RESPONSE: Dict[int | str, Dict[str, Any]] = {
    404: {"description": "Not found"}
}

router = APIRouter()

router.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"],
    responses=NOT_FOUND_RESPONSE,
)


router.include_router(
    user.router,
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)
