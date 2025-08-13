from typing import Any, Dict

from fastapi import APIRouter

from app.api.routers import auth, user, hospital, rbac_test

NOT_FOUND_RESPONSE: Dict[int | str, Dict[str, Any]] = {
    404: {"description": "Not found"}
}

router = APIRouter()

router.include_router(
    auth.router,
    responses=NOT_FOUND_RESPONSE,
)


router.include_router(
    user.router,
    responses=NOT_FOUND_RESPONSE,
)

router.include_router(
    hospital.router,
    responses=NOT_FOUND_RESPONSE,
)

router.include_router(
    rbac_test.router,
    responses=NOT_FOUND_RESPONSE,
)
