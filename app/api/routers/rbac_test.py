from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.utils.constant.roles import RoleChecks

router = APIRouter()


@router.get("/admin", dependencies=[RoleChecks.ADMIN])
async def admin_access(db: Session = Depends(get_db)):
    return {"msg": "This is admin access point"}


@router.get("/nurse", dependencies=[RoleChecks.NURSE])
async def nurse_access(db: Session = Depends(get_db)):
    return {"msg": "This is nurse access point"}


@router.get("/ipc_officer", dependencies=[RoleChecks.IPC_OFFICER])
async def ipc_officer_access(db: Session = Depends(get_db)):
    return {"msg": "This is IPC officer access point"}


@router.get("/hospital_admin", dependencies=[RoleChecks.HOSPITAL_ADMIN])
async def hospital_admin_access(db: Session = Depends(get_db)):
    return {"msg": "This is hospital admin access point"}


@router.get("/superadmin", dependencies=[RoleChecks.SUPERADMIN])
async def superadmin_access(db: Session = Depends(get_db)):
    return {"msg": "This is superadmin access point"}
