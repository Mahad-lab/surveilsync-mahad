from sqlalchemy.orm import Session
from app.models.hospital import Hospital

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
