from fastapi import HTTPException


def require_admin(role: str) -> None:
    if role != "admin":
        raise HTTPException(status_code=403, detail="admin role required")


def require_student(role: str) -> None:
    if role != "student":
        raise HTTPException(status_code=403, detail="student role required")
