from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.todo import Todo

class TodoRepository:
    def __init__(self, db:Session) -> None:
        self.db = db


    def list_todos(self, limit: int, offset: int, done: Optional[bool],owner_id: int) -> list[Todo]:
        # 基础查询
        stmt = select(Todo).where(Todo.owner_id == owner_id).offset(offset).limit(limit)

        if done is not None:
            stmt = stmt.where(Todo.done == done)

        return self.db.scalars(stmt).all()
    
    def create_todo(self, title: str,owner_id: int) -> Todo:
        # 新建ORM 对象并写入数据库
        todo = Todo(title=title, done=False, owner_id=owner_id)
        self.db.add(todo)
        self.db.commit()
        self.db.refresh(todo)
        return todo