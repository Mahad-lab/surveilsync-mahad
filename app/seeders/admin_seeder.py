from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.user import User
from app.utils.constant.globals import UserRole

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AdminSeeder:
    @staticmethod
    def seed(db: Session) -> None:
        """
        Seed an admin user if no admin exists in the database
        """
        # Check if admin user exists
        admin_exists = db.query(User).filter(User.role == UserRole.ADMIN).first()
        if not admin_exists:
            # Create admin user
            hashed_password = pwd_context.hash("admin")
            admin_user = User(
                email="admin@admin.com",
                password=hashed_password,
                first_name="Super",
                last_name="Admin",
                role=UserRole.ADMIN,
                is_active=True,
            )
            db.add(admin_user)
            db.commit()
            print("Admin user created successfully")
        else:
            print("Admin user already exists")
