from datetime import datetime

from pydantic import BaseModel

from app.schemas.user import UserCreate


class HospitalBase(BaseModel):
    name: str


class HospitalCreate(HospitalBase):
    pass


class HospitalUpdate(HospitalBase):
    pass


class Hospital(HospitalBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool = True
    admin: int | None = None

    class Config:
        from_attributes = True


class HospitalAdminCreate(UserCreate):
    hospital_id: int

