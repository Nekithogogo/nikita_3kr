from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    hashed_password: str
    role: str = "user"

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class SQLiteUserCreate(BaseModel):
    username: str
    password: str

class TodoBase(BaseModel):
    title: str
    description: str

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class Todo(TodoBase):
    id: int
    completed: bool = False

    class Config:
        from_attributes = True