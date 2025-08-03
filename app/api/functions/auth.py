from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.api.functions.user import get_user_by_email, get_user_by_id
from app.core.dependencies import get_db, oauth2_scheme
from app.schemas.user import Token
from app.utils.env import (
    ACCESS_TOKEN_EXPIRE_DAYS,
    ALGORITHM,
    REFRESH_SECRET_KEY,
    SECRET_KEY,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# =====================> login/logout <============================
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(db: Session, user: OAuth2PasswordRequestForm):
    member = await get_user_by_email(db, user.username)
    if not member:
        return False
    if not verify_password(user.password, member.password):
        return False
    return member


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def refresh_access_token(db: Session, refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str | int | None = payload.get("id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        # member = await User.get(user_id)
        member = await get_user_by_id(db, int(user_id))
        if member is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
        access_token = create_access_token(
            data={"id": member.id, "email": member.email, "role": member.role},
            expires_delta=access_token_expires,
        )
        return Token(
            access_token=access_token, refresh_token=refresh_token, token_type="bearer"
        )
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


# get current users info
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # print(f"Payload =====> {payload}")
        current_email: str | None = payload.get("email")
        if current_email is None:
            raise credentials_exception
        user = await get_user_by_email(db, current_email)
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception
