from sqlalchemy.orm import Session
from app.models.hospital import Hospital
from app.utils.constant.roles import UserRole
from app.models.user import User


# Create a new hospital
def create_hospital(db: Session, name: str) -> Hospital:
    hospital = Hospital(name=name)
    db.add(hospital)
    db.commit()
    db.refresh(hospital)
    return hospital


# Get hospital by id
def get_hospital(db: Session, hospital_id: int) -> Hospital:
    return db.query(Hospital).filter(Hospital.id == hospital_id).first()


# Get all hospitals
def get_hospitals(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Hospital).offset(skip).limit(limit).all()


# Update hospital
def update_hospital(db: Session, hospital_id: int, name: str) -> Hospital:
    hospital = get_hospital(db, hospital_id)
    if hospital:
        hospital.name = name
        db.commit()
        db.refresh(hospital)
    return hospital


# Delete hospital
def delete_hospital(db: Session, hospital_id: int) -> bool:
    hospital = get_hospital(db, hospital_id)
    if hospital:
        # db.delete(hospital)
        hospital.is_active = False  # Soft delete
        db.add(hospital)
        db.commit()
        db.refresh(hospital)
        return True
    return False





# Get hospital admin
def get_hospital_admin(db: Session, hospital_id: int) -> User:
    hospital = db.query(Hospital).filter(Hospital.id == hospital_id).first()
    if hospital and hospital.admin:
        return db.query(User).filter(User.id == hospital.admin, User.role == UserRole.HOSPITAL_ADMIN).first()
    return None


# Assign admin to hospital
def assign_hospital_admin(db: Session, hospital_id: int, user_id: int) -> Hospital:
    hospital = get_hospital(db, hospital_id)
    if hospital:
        if hospital.admin:
            raise ValueError("Hospital already has an admin")
        hospital.admin = user_id
        db.commit()
        db.refresh(hospital)
        return hospital
    return None


# Update hospital admin
def update_hospital_admin(db: Session, hospital_id: int, admin_id: int) -> Hospital:
    hospital = get_hospital(db, hospital_id)
    if hospital:
        hospital.admin = admin_id
        db.commit()
        db.refresh(hospital)
        return hospital
    return None


# Delete hospital admin
def delete_hospital_admin(db: Session, hospital_id: int) -> bool:
    hospital = get_hospital(db, hospital_id)
    if hospital and hospital.admin:
        hospital.admin = None  # Remove admin
        db.add(hospital)
        db.commit()
        db.refresh(hospital)
        return True
    return False


# Get users in a hospital
def get_hospital_users(db: Session, hospital_id: int, skip: int = 0, limit: int = 100):
    hospital = db.query(Hospital).filter(Hospital.id == hospital_id).first()
    if not hospital or not hospital.admin:
        return []
    user = db.query(User).filter(User.id == hospital.admin).first()
    return [user] if user else []