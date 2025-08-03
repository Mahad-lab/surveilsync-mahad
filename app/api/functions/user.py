from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.user import User as UserModel
from app.schemas.user import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# get user by email
async def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()


# get user by id
async def get_user_by_id(db: Session, user_id: int):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# crete new user
def create_new_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    new_user = UserModel(
        email=user.email,
        password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# get all user
def read_all_user(db: Session, skip: int, limit: int):
    return db.query(UserModel).offset(skip).limit(limit).all()


# update user
async def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = await get_user_by_id(db, user_id)
    updated_data = user.model_dump(exclude_unset=True)  # partial update
    for key, value in updated_data.items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# delete user
async def delete_user(db: Session, user_id: int):
    db_user = await get_user_by_id(db, user_id)
    db.delete(db_user)
    db.commit()
    # db.refresh(db_user)
    return {"msg": f"{db_user.email} deleted successfully"}
