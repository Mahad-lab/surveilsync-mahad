from datetime import datetime

from pydantic import BaseModel


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

    class Config:
        from_attributes = True
