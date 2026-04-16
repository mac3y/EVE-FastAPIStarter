from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime

class TodoBase(SQLModel):
    title: str = Field(index=True)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    user_id: int = Field(foreign_key="user.id")

class Todo(TodoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)