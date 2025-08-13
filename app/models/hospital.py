from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base

from .common import CommonModel


class Hospital(CommonModel):
    __tablename__ = "hospitals"

    name = Column(String(100), nullable=False)
    admin = Column(ForeignKey("users.id"), unique=True, nullable=True)

    # Relationships
    admin_user = relationship("User", back_populates="hospital")

    def __repr__(self):
        return f"{self.name}"


metadata = Base.metadata
