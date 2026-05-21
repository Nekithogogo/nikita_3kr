from fastapi import APIRouter, Depends, HTTPException, status, Request
from auth import authenticate_user_basic, get_current_user, fake_users_db
from security import get_password_hash, create_access_token, verify_password
from models import UserCreate, UserInDB, Token
from rate_limit import limiter
import secrets

router = APIRouter(tags=["Authentication (JWT & Basic)"])

# 6.1 — секретное сообщение через Basic auth
@router.get("/secret")
async def get_secret(user: UserInDB = Depends(authenticate_user_basic)):
    return {"message": "You got my secret, welcome"}

# 6.2 — GET /basic-login (приветствие через Basic auth)
@router.get("/basic-login")
async def basic_login(user: UserInDB = Depends(authenticate_user_basic)):
    return {"message": f"Welcome, {user.username}!"}

# 6.5 — регистрация (с хешированием, rate limit 1/мин)
@router.post("/register", status_code=status.HTTP_201_CREATED)
@limiter.limit("1/minute")
async def register_user(request: Request, user_data: UserCreate):
    if user_data.username in fake_users_db:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    hashed = get_password_hash(user_data.password)
    fake_users_db[user_data.username] = UserInDB(username=user_data.username, hashed_password=hashed, role="user")
    return {"message": "New user created"}

# 6.5 — JWT логин (rate limit 5/мин)
@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
async def login(request: Request, user_data: UserCreate):
    user = fake_users_db.get(user_data.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not secrets.compare_digest(user_data.username, user.username):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization failed")
    if not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization failed")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# 6.4 — защищённый ресурс (JWT)
@router.get("/protected_resource")
async def protected_resource(current_user: UserInDB = Depends(get_current_user)):
    return {"message": "Access granted"}