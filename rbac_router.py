from fastapi import APIRouter, Depends
from auth import get_current_user
from rbac import require_role, require_any_role
from models import UserInDB

router = APIRouter(tags=["RBAC"])

@router.get("/admin/resource")
async def admin_resource(current_user: UserInDB = Depends(require_role("admin"))):
    return {"message": f"Welcome admin {current_user.username}, you have full access"}

@router.get("/user/resource")
async def user_resource(current_user: UserInDB = Depends(require_any_role(["user", "admin"]))):
    return {"message": f"Hello {current_user.username}, you can read/update resources"}

@router.get("/guest/resource")
async def guest_resource(current_user: UserInDB = Depends(require_role("guest"))):
    return {"message": "Guest read-only access"}

@router.post("/admin/resource")
async def create_resource(current_user: UserInDB = Depends(require_role("admin"))):
    return {"message": "Resource created by admin"}