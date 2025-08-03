from typing import Annotated

# fastapi
from fastapi import APIRouter, Depends, HTTPException

# sqlalchemy
from sqlalchemy.orm import Session

from app.api.functions import auth as auth_functions
from app.api.functions import user as user_functions

# import
from app.core.dependencies import get_db
from app.core.rolechecker import RoleChecker
from app.schemas.pagination import PaginationParams
from app.schemas.user import User, UserCreate, UserUpdate

router = APIRouter()


# @user_module.get('/')
# async def read_auth_page():
#     return {"msg": "Auth page Initialization done"}


# get current user
@router.get("/me/", response_model=User)
async def read_current_user(
    current_user: Annotated[User, Depends(auth_functions.get_current_user)],
):
    return current_user


# create new user
@router.post("/", response_model=User)
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = await user_functions.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    new_user = user_functions.create_new_user(db, user)
    return new_user


# get all user
@router.get(  # TODO: chnage pagination response to use genetic
    "/", response_model=list[User], dependencies=[Depends(RoleChecker(["admin"]))]
)
async def read_all_user(
    pagination: PaginationParams = Depends(), db: Session = Depends(get_db)
):
    return user_functions.read_all_user(db, pagination.page, pagination.size)


# get user by id
@router.get(
    "/{user_id}/",
    response_model=User,
    dependencies=[Depends(RoleChecker(["admin", "user"]))],
)
async def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    return await user_functions.get_user_by_id(db, user_id)


# update user
@router.patch(
    "/{user_id}/", response_model=User, dependencies=[Depends(RoleChecker(["admin"]))]
)
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    print(f"Received data: {user.model_dump()}")
    return await user_functions.update_user(db, user_id, user)


# delete user
@router.delete(
    "/{user_id}/",
    #    response_model=User,
    dependencies=[Depends(RoleChecker(["admin"]))],
)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted_user = await user_functions.delete_user(db, user_id)

    return deleted_user
