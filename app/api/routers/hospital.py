from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from app.core.dependencies import get_db
from app.api.functions import hospital as hospital_crud
from app.schemas.hospital import Hospital, HospitalCreate, HospitalUpdate
from app.schemas.pagination import PaginationParams, PaginationResponse
from app.utils.constant.roles import RoleChecks

router = APIRouter(
    prefix="/hospitals", tags=["hospitals"], dependencies=[RoleChecks.PROJECT_ADMIN]
)


@router.post("/", response_model=Hospital)
async def create_hospital(hospital: HospitalCreate, db: Session = Depends(get_db)):
    return hospital_crud.create_hospital(db=db, name=hospital.name)


@router.get("/{hospital_id}/", response_model=Hospital)
async def read_hospital(
    hospital_id: int,
    db: Session = Depends(get_db),
    depends=[RoleChecks.HOSPITAL_ADMIN, RoleChecks.PROJECT_ADMIN],
):
    hospital = hospital_crud.get_hospital(db=db, hospital_id=hospital_id)
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return hospital


@router.get("/", response_model=PaginationResponse[Hospital])
async def read_hospitals(
    pagination: PaginationParams = Depends(), db: Session = Depends(get_db)
):
    skip = (pagination.page - 1) * pagination.size
    try:
        items = hospital_crud.get_hospitals(db=db, skip=skip, limit=pagination.size)
        return PaginationResponse(
            items=items,
            total=db.query(hospital_crud.Hospital).count(),
            page=pagination.page,
            size=pagination.size,
        )
    except Exception as e:
        print(f"Error fetching hospitals: {e}")
        raise HTTPException(status_code=500, detail="Error fetching hospitals")


@router.put("/{hospital_id}/", response_model=Hospital)
async def update_hospital(
    hospital_id: int,
    hospital: HospitalUpdate,
    db: Session = Depends(get_db),
    depends=[RoleChecks.HOSPITAL_ADMIN, RoleChecks.PROJECT_ADMIN],
):
    updated_hospital = hospital_crud.update_hospital(
        db=db, hospital_id=hospital_id, name=hospital.name
    )
    if not updated_hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return updated_hospital


@router.delete("/{hospital_id}/", response_model=dict)
async def delete_hospital(hospital_id: int, db: Session = Depends(get_db)):
    success = hospital_crud.delete_hospital(db=db, hospital_id=hospital_id)
    if not success:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return {"detail": "Hospital deleted successfully"}
