from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.todo_service import TodoService
from app.repositories.todo_repository import TodoRepository

def get_todo_service(db: Session = Depends(get_db)) -> TodoService:
    # 在依赖层组装 service + repository + db session
    repo = TodoRepository(db)
    return TodoService(repo=repo)
