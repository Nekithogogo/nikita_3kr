from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPBearer, HTTPAuthorizationCredentials
import secrets
from security import verify_password, get_password_hash, decode_access_token
from models import UserInDB
from typing import Dict

fake_users_db: Dict[str, UserInDB] = {
    "admin": UserInDB(username="admin", hashed_password=get_password_hash("admin123"), role="admin"),
    "user":   UserInDB(username="user",   hashed_password=get_password_hash("user123"),   role="user"),
    "guest":  UserInDB(username="guest",  hashed_password=get_password_hash("guest123"),  role="guest"),
}

security_basic = HTTPBasic()
security_bearer = HTTPBearer(auto_error=False)

def authenticate_user_basic(credentials: HTTPBasicCredentials = Depends(security_basic)) -> UserInDB:
    user = fake_users_db.get(credentials.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    if not secrets.compare_digest(credentials.username, user.username):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security_bearer)) -> UserInDB:
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = decode_access_token(credentials.credentials)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    username = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = fake_users_db.get(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user