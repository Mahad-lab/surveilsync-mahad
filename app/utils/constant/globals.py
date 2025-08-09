from enum import Enum as PythonEnum

class UserRole(str, PythonEnum):
    ADMIN = "admin"  # TODO: remove this role

    NURSE = "nurse"
    IPC_OFFICER = "ipc_officer"
    HOSPITAL_ADMIN = "hospital_admin"
    PROJECT_ADMIN = "project_admin"
