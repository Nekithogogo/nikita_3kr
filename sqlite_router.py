from fastapi import APIRouter, Depends, HTTPException, status
from database import get_db_connection
from models import SQLiteUserCreate
import sqlite3

router = APIRouter(tags=["SQLite (8.1)"])

@router.post("/register-sqlite", status_code=status.HTTP_201_CREATED)
async def register_sqlite(user: SQLiteUserCreate):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (user.username, user.password)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
    return {"message": "User registered successfully!"}