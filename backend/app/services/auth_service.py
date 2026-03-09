from app.core.security import hash_password
from app.repositories.user_repository import UserRepository
from app.core.exceptions import AppException
from app.core.security import hash_password
from app.repositories.user_repository import UserRepository

class AuthService:
    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    def register_user(self, username: str, password: str) -> dict:
        # 注册前先检查用户名是否存在
        existed = self.user_repo.get_by_username(username)
        if existed is not None:
            raise AppException(
                code="USERNAME_ALREADY_EXISTS",
                message="Username already exists",
                status_code=409,
            )

        
        password_hash = hash_password(password)
        user = self.user_repo.create_user(username=username, password_hash=password_hash)

        return {"id": user.id, "username": user.username}
