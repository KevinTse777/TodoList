from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_username(self, username:str) -> Optional[User]:
        # 登陆/注册前置检查： 按用户名查唯一用户
        stmt = select(User).where(User.username == username)
        return self.db.scalar(stmt)
    
    def create_user(self, username: str, password_hash: str) -> User:
        # 注册： 写入用户记录 （密码只存哈希）
        user = User(username=username, password_hash=password_hash)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user