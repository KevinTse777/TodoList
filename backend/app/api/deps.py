from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.todo_service import TodoService
from app.repositories.todo_repository import TodoRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService


def get_todo_service(db: Session = Depends(get_db)) -> TodoService:
    # 在依赖层组装 service + repository + db session
    repo = TodoRepository(db)
    return TodoService(repo=repo)

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    # 组装认证服务依赖链
    user_repo = UserRepository(db)
    return AuthService(user_repo=user_repo)