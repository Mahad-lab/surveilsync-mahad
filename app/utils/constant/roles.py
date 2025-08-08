from fastapi import Depends

from app.core.rolechecker import RoleChecker
from app.models.user import UserRole


class RoleChecks:
    ADMIN = Depends(RoleChecker([UserRole.ADMIN]))
    USER = Depends(RoleChecker([UserRole.USER]))

    NURSE = Depends(RoleChecker([UserRole.NURSE]))
    IPC_OFFICER = Depends(RoleChecker([UserRole.IPC_OFFICER]))
    HOSPITAL_ADMIN = Depends(RoleChecker([UserRole.HOSPITAL_ADMIN]))
    SUPERADMIN = Depends(RoleChecker([UserRole.SUPERADMIN]))

    @staticmethod
    def custom(roles: list[UserRole]):
        return Depends(RoleChecker(roles))
