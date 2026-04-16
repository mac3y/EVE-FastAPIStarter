from sqlmodel import Session, select, func
from app.models.todo import Todo, TodoBase
from typing import Optional, Tuple, List
from app.utilities.pagination import Pagination
import logging

logger = logging.getLogger(__name__)

class TodoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, todo_data: TodoBase, user_id: int) -> Optional[Todo]:
        try:
            todo = Todo.model_validate(todo_data)
            todo.user_id = user_id
            self.db.add(todo)
            self.db.commit()
            self.db.refresh(todo)
            return todo
        except Exception as e:
            logger.error(f"An error occurred while saving todo: {e}")
            self.db.rollback()
            raise

    def get_by_id(self, todo_id: int, user_id: int) -> Optional[Todo]:
        return self.db.exec(
            select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
        ).one_or_none()

    def get_user_todos(self, user_id: int, page: int = 1, limit: int = 10) -> Tuple[List[Todo], Pagination]:
        offset = (page - 1) * limit
        db_qry = select(Todo).where(Todo.user_id == user_id).order_by(Todo.created_at.desc())
        
        count_qry = select(func.count()).select_from(db_qry.subquery())
        count_todos = self.db.exec(count_qry).one()

        todos = self.db.exec(db_qry.offset(offset).limit(limit)).all()
        pagination = Pagination(total_count=count_todos, current_page=page, limit=limit)

        return todos, pagination

    def get_all_user_todos(self, user_id: int) -> List[Todo]:
        return self.db.exec(
            select(Todo).where(Todo.user_id == user_id).order_by(Todo.created_at.desc())
        ).all()

    def update_todo_status(self, todo_id: int, user_id: int, completed: bool) -> Optional[Todo]:
        todo = self.get_by_id(todo_id, user_id)
        if not todo:
            return None
        
        todo.completed = completed
        try:
            self.db.add(todo)
            self.db.commit()
            self.db.refresh(todo)
            return todo
        except Exception as e:
            logger.error(f"An error occurred while updating todo: {e}")
            self.db.rollback()
            raise

    def delete_todo(self, todo_id: int, user_id: int) -> bool:
        todo = self.get_by_id(todo_id, user_id)
        if not todo:
            return False
        
        try:
            self.db.delete(todo)
            self.db.commit()
            return True
        except Exception as e:
            logger.error(f"An error occurred while deleting todo: {e}")
            self.db.rollback()
            raise