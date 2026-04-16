from app.repositories.todo import TodoRepository
from app.models.todo import TodoBase, Todo
from app.schemas.todo import TodoCreate
from typing import List, Optional
from datetime import datetime

class TodoService:
    def __init__(self, todo_repo: TodoRepository):
        self.todo_repo = todo_repo

    def create_todo(self, todo_data: TodoCreate, user_id: int) -> Todo:
        # Convert TodoCreate to TodoBase (without user_id)
        todo_base = TodoBase(
            title=todo_data.title,
            description=todo_data.description,
            completed=False,
            created_at=datetime.now(),
            user_id=user_id  # Add user_id here!
        )
        return self.todo_repo.create(todo_base, user_id)

    def get_user_todos(self, user_id: int) -> List[Todo]:
        return self.todo_repo.get_all_user_todos(user_id)

    def toggle_todo_status(self, todo_id: int, user_id: int) -> Optional[Todo]:
        todo = self.todo_repo.get_by_id(todo_id, user_id)
        if not todo:
            return None
        return self.todo_repo.update_todo_status(todo_id, user_id, not todo.completed)

    def delete_todo(self, todo_id: int, user_id: int) -> bool:
        return self.todo_repo.delete_todo(todo_id, user_id)