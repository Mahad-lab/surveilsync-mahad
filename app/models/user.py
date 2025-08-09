from sqlalchemy import Column, Enum, String

from app.core.database import Base
from app.utils.constant.globals import UserRole

from .common import CommonModel


class User(CommonModel):
    __tablename__ = "users"

    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    email = Column(String(50), unique=True, index=True)
    password = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER)

    def __repr__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


metadata = Base.metadata
