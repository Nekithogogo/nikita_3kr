from fastapi import APIRouter, Depends, HTTPException, status
from database import get_db_connection
from models import Todo, TodoCreate, TodoUpdate

router = APIRouter(prefix="/todos", tags=["Todos (8.2)"])

@router.post("/", response_model=Todo, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoCreate):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO todos (title, description, completed) VALUES (?, ?, ?)",
            (todo.title, todo.description, False)
        )
        conn.commit()
        todo_id = cursor.lastrowid
        cursor.execute("SELECT id, title, description, completed FROM todos WHERE id = ?", (todo_id,))
        row = cursor.fetchone()
        return Todo(id=row["id"], title=row["title"], description=row["description"], completed=bool(row["completed"]))

@router.get("/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, description, completed FROM todos WHERE id = ?", (todo_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
        return Todo(id=row["id"], title=row["title"], description=row["description"], completed=bool(row["completed"]))

@router.put("/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo_update: TodoUpdate):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM todos WHERE id = ?", (todo_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

        update_fields = []
        values = []
        if todo_update.title is not None:
            update_fields.append("title = ?")
            values.append(todo_update.title)
        if todo_update.description is not None:
            update_fields.append("description = ?")
            values.append(todo_update.description)
        if todo_update.completed is not None:
            update_fields.append("completed = ?")
            values.append(1 if todo_update.completed else 0)

        if not update_fields:
            cursor.execute("SELECT id, title, description, completed FROM todos WHERE id = ?", (todo_id,))
            row = cursor.fetchone()
            return Todo(id=row["id"], title=row["title"], description=row["description"], completed=bool(row["completed"]))

        values.append(todo_id)
        query = f"UPDATE todos SET {', '.join(update_fields)} WHERE id = ?"
        cursor.execute(query, values)
        conn.commit()

        cursor.execute("SELECT id, title, description, completed FROM todos WHERE id = ?", (todo_id,))
        row = cursor.fetchone()
        return Todo(id=row["id"], title=row["title"], description=row["description"], completed=bool(row["completed"]))

@router.delete("/{todo_id}", status_code=status.HTTP_200_OK)
async def delete_todo(todo_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
        conn.commit()
    return {"message": "Todo deleted successfully"}