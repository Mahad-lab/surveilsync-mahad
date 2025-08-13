from sqlalchemy import Column, String

from app.core.database import Base

from .common import CommonModel


class Hospital(CommonModel):
    __tablename__ = "hospitals"

    name = Column(String(100), nullable=False)

    def __repr__(self):
        return f"{self.name}"


metadata = Base.metadata
