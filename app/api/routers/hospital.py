from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from app.core.dependencies import get_db
from app.api.functions import hospital as hospital_crud
from app.api.functions import user as user_crud
from app.schemas.hospital import Hospital, HospitalCreate, HospitalUpdate, HospitalAdminCreate
from app.schemas.pagination import PaginationParams, PaginationResponse
from app.schemas.user import User as UserResponse
from app.utils.constant.roles import RoleChecks

router = APIRouter(prefix="/hospitals", tags=["hospitals"])


@router.post("/", response_model=Hospital, dependencies=[RoleChecks.PROJECT_ADMIN])
async def create_hospital(hospital: HospitalCreate, db: Session = Depends(get_db)):
    return hospital_crud.create_hospital(db=db, name=hospital.name)


@router.get(
    "/{hospital_id}/",
    response_model=Hospital,
    dependencies=[RoleChecks.PROJECT_ADMIN_OR_HOSPITAL_ADMIN],
)
async def read_hospital(
    hospital_id: int,
    db: Session = Depends(get_db),
):
    hospital = hospital_crud.get_hospital(db=db, hospital_id=hospital_id)
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return hospital


@router.get(
    "/",
    response_model=PaginationResponse[Hospital],
    dependencies=[RoleChecks.PROJECT_ADMIN],
)
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


@router.put(
    "/{hospital_id}/",
    response_model=Hospital,
    dependencies=[RoleChecks.PROJECT_ADMIN_OR_HOSPITAL_ADMIN],
)
async def update_hospital(
    hospital_id: int,
    hospital: HospitalUpdate,
    db: Session = Depends(get_db),
):
    updated_hospital = hospital_crud.update_hospital(
        db=db, hospital_id=hospital_id, name=hospital.name
    )
    if not updated_hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return updated_hospital


@router.delete(
    "/{hospital_id}/", response_model=dict, dependencies=[RoleChecks.PROJECT_ADMIN]
)
async def delete_hospital(hospital_id: int, db: Session = Depends(get_db)):
    success = hospital_crud.delete_hospital(db=db, hospital_id=hospital_id)
    if not success:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return {"detail": "Hospital deleted successfully"}


# HOSPITAL ADMINISTRATION ENDPOINTS


@router.post(
    "/{hospital_id}/admin",
    response_model=Hospital,
    dependencies=[RoleChecks.PROJECT_ADMIN],
)
async def create_hospital_admin(
    user: HospitalAdminCreate = Depends(HospitalAdminCreate),
    db: Session = Depends(get_db),
):
    try:
        hospital = hospital_crud.get_hospital(db=db, hospital_id=user.hospital_id)
        if not hospital:
            raise HTTPException(status_code=404, detail="Hospital not found")
        
        # Check if the hospital already has an admin
        if hospital.admin:
            raise ValueError("Hospital already has an admin")

        # get user by email
        existing_user = await user_crud.get_user_by_email(db=db, email=user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email already exists")

        # Create the admin user
        admin_user = user_crud.create_new_user(
            db=db,
            user=user,
        ) 
        hospital = hospital_crud.assign_hospital_admin(
            db=db, hospital_id=hospital.id, user_id=admin_user.id
        )
        return hospital
    except ValueError as e:
        print(f"Error assigning hospital admin: {e}")
        raise HTTPException(status_code=400, detail="Hospital already has an admin")
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e  # Re-raise HTTP exceptions
        # Log the error and raise a generic HTTP exception
        print(f"Error assigning hospital admin: {e}")
        raise HTTPException(status_code=500, detail="Error assigning hospital admin")


@router.get(
    "/{hospital_id}/admin",
    response_model=UserResponse,
    dependencies=[RoleChecks.PROJECT_ADMIN],
)
async def read_hospital_admin(
    hospital_id: int,
    db: Session = Depends(get_db),
):
    hospital = hospital_crud.get_hospital_admin(db=db, hospital_id=hospital_id)
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital admin not found")
    return hospital


@router.put(
    "/{hospital_id}/admin",
    response_model=Hospital,
    dependencies=[RoleChecks.PROJECT_ADMIN],
)
async def update_hospital_admin(
    hospital_id: int,
    admin_id: int,
    db: Session = Depends(get_db),
):
    updated_hospital = hospital_crud.update_hospital_admin(
        db=db, hospital_id=hospital_id, admin_id=admin_id
    )
    if not updated_hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return updated_hospital


@router.delete(
    "/{hospital_id}/admin", response_model=dict, dependencies=[RoleChecks.PROJECT_ADMIN]
)
async def delete_hospital_admin(hospital_id: int, db: Session = Depends(get_db)):
    success = hospital_crud.delete_hospital_admin(db=db, hospital_id=hospital_id)
    if not success:
        raise HTTPException(status_code=404, detail="Hospital admin not found")
    return {"detail": "Hospital admin deleted successfully"}


@router.get(
    "/{hospital_id}/users",
    response_model=PaginationResponse[UserResponse],
    dependencies=[RoleChecks.PROJECT_ADMIN_OR_HOSPITAL_ADMIN],
)
async def read_hospital_users(
    hospital_id: int,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
):
    skip = (pagination.page - 1) * pagination.size
    try:
        items = hospital_crud.get_hospital_users(
            db=db, hospital_id=hospital_id, skip=skip, limit=pagination.size
        )
        total = 1 if items else 0  # Only admin user is linked to hospital
        return PaginationResponse(
            items=items,
            total=total,
            page=pagination.page,
            size=pagination.size,
        )
    except Exception as e:
        print(f"Error fetching hospital users: {e}")
        raise HTTPException(status_code=500, detail="Error fetching hospital users")
