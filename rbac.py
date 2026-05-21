from fastapi import Depends, HTTPException, status
from auth import get_current_user
from models import UserInDB

def require_role(required_role: str):
    def role_checker(current_user: UserInDB = Depends(get_current_user)):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{required_role}' required"
            )
        return current_user
    return role_checker

def require_any_role(allowed_roles: list):
    def role_checker(current_user: UserInDB = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Allowed roles: {allowed_roles}"
            )
        return current_user
    return role_checker