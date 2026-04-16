from fastapi import Request, Depends, HTTPException, status
from app.dependencies import SessionDep
from app.dependencies.auth import AuthDep
from . import api_router
from app.services.todo_service import TodoService
from app.repositories.todo import TodoRepository
from app.schemas.todo import TodoCreate, TodoResponse
from typing import List


@api_router.get("/todos", response_model=List[TodoResponse])
async def get_user_todos(request: Request, db: SessionDep, user: AuthDep):
    todo_repo = TodoRepository(db)
    todo_service = TodoService(todo_repo)
    todos = todo_service.get_user_todos(user.id)
    return todos


@api_router.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo_data: TodoCreate, 
    db: SessionDep, 
    user: AuthDep
):
    todo_repo = TodoRepository(db)
    todo_service = TodoService(todo_repo)
    
    todo = todo_service.create_todo(todo_data, user.id)
    return todo


@api_router.post("/todos/{todo_id}/toggle", response_model=TodoResponse)
async def toggle_todo(
    todo_id: int, 
    db: SessionDep, 
    user: AuthDep
):
    todo_repo = TodoRepository(db)
    todo_service = TodoService(todo_repo)
    
    todo = todo_service.toggle_todo_status(todo_id, user.id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@api_router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: int, 
    db: SessionDep, 
    user: AuthDep
):
    todo_repo = TodoRepository(db)
    todo_service = TodoService(todo_repo)
    
    deleted = todo_service.delete_todo(todo_id, user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Todo not found")
    return None