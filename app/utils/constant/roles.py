from fastapi import Depends

from app.core.rolechecker import RoleChecker
from app.models.user import UserRole


class RoleChecks:
    ADMIN = Depends(RoleChecker([UserRole.ADMIN]))

    NURSE = Depends(RoleChecker([UserRole.NURSE]))
    IPC_OFFICER = Depends(RoleChecker([UserRole.IPC_OFFICER]))
    HOSPITAL_ADMIN = Depends(RoleChecker([UserRole.HOSPITAL_ADMIN]))
    PROJECT_ADMIN = Depends(RoleChecker([UserRole.PROJECT_ADMIN]))

    PROJECT_ADMIN_OR_HOSPITAL_ADMIN = Depends(
        RoleChecker([UserRole.PROJECT_ADMIN, UserRole.HOSPITAL_ADMIN])
    )

    @staticmethod
    def custom(roles: list[UserRole]):
        return Depends(RoleChecker(roles))
