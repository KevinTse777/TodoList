from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.todo import Todo

class TodoRepository:
    def __init__(self, db:Session) -> None:
        self.db = db


    def list_todos(self, limit: int, offset: int, done: Optional[bool]) -> list[Todo]:
        # 基础查询
        stmt = select(Todo).offset(offset).limit(limit)

        if done is not None:
            stmt = stmt.where(Todo.done == done)

        return self.db.scalars(stmt).all()