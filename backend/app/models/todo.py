from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class todo(Base):
    __tablename__ = "todos"

    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    done: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


    #owner_id 是权限隔离核心字段： 后续所有查询都按 owner_id 过滤
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", nullable=False, index=True))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    updated_at:Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now, nullable=False
    )

    owner = relationship("User", back_populates="todos")