from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.todo_service import TodoService
from app.repositories.todo_repository import TodoRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.models.user import User
from app.core.security import decode_access_token
from app.core.exceptions import AppException


def get_todo_service(db: Session = Depends(get_db)) -> TodoService:
    # 在依赖层组装 service + repository + db session
    repo = TodoRepository(db)
    return TodoService(repo=repo)

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    # 组装认证服务依赖链
    user_repo = UserRepository(db)
    return AuthService(user_repo=user_repo)

# tokenUrl 指向你的登录接口，供 OpenAPI 文档识别 OAuth2 密码模式
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    # 解码验签 JWT
    payload = decode_access_token(token)
    username = payload.get("sub")
    if not username:
        raise AppException(
            code="INVALID_TOKEN",
            message="Token payload missing subject",
            status_code=401
        )
    
    user = UserRepository(db).get_by_username(username)
    if user is None:
        raise AppException(
            code="USER_NOT_FOUND",
            message="User from token does not exist",
            status_code=401,
        )

    return user