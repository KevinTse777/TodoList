from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, func

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # 用户名唯一
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    # 储存密码哈希，禁止铭文
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    # 用户状态：后续可用于禁用账户
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    #更新时间
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    #反向关系：一个用户多个todo
    todos = relationship("Todo", back_populates="owner", cascade="all, delete-orphan")