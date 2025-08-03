# fastapi
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

# sqlalchemy
from sqlalchemy.orm import Session

from app.api.functions import auth as auth_functions
from app.core.dependencies import get_db

# import
from app.schemas.user import Token
from app.utils.env import (
    ACCESS_TOKEN_EXPIRE_DAYS,
    REFRESH_TOKEN_EXPIRE_DAYS,
)

router = APIRouter()


# ============> login/logout < ======================
# getting access token for login
@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> Token:
    member = await auth_functions.authenticate_user(db, user=form_data)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = auth_functions.create_access_token(
        data={"id": member.id, "email": member.email, "role": member.role},
        expires_delta=access_token_expires,
    )

    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = await auth_functions.create_refresh_token(
        data={"id": member.id, "email": member.email, "role": member.role},
        expires_delta=refresh_token_expires,
    )
    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )


@router.post("/refresh", response_model=Token)
async def refresh_access_token(refresh_token: str, db: Session = Depends(get_db)):
    token = await auth_functions.refresh_access_token(db, refresh_token)
    return token
