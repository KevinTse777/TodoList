from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.todo_service import TodoService

def get_todo_service(db: Session = Depends(get_db)) -> TodoService:
    # 先把DB会话注入链路打通
    _ = db
    return TodoService()
