from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.seeders.admin_seeder import AdminSeeder


class DatabaseSeeder:
    """Main seeder class that runs all seeders"""

    @staticmethod
    def run() -> None:
        """
        Run all seeders in the correct order
        """
        db = SessionLocal()
        try:
            # Register all seeders here
            DatabaseSeeder._run_seeders(
                db,
                [
                    AdminSeeder,
                    # Add more seeders here
                ],
            )
        finally:
            db.close()

    @staticmethod
    def _run_seeders(db: Session, seeders: list) -> None:
        """
        Run each seeder in the provided list
        """
        for seeder in seeders:
            try:
                seeder.seed(db)
            except Exception as e:
                print(f"Error running {seeder.__name__}: {str(e)}")
