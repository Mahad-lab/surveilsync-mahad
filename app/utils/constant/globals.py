from enum import Enum as PythonEnum

class UserRole(str, PythonEnum):
    USER = "user"
    ADMIN = "admin"  # TODO: remove this role

    NURSE = "nurse"
    IPC_OFFICER = "ipc_officer"
    HOSPITAL_ADMIN = "hospital_admin"
    SUPERADMIN = "superadmin"
