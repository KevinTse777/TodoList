from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


from app.core.config import(
    DATABASE_URL,
    DB_MAX_OVERFLOW,
    DB_POOL_PRE_PING,
    DB_POOL_RECYCLE,
    DB_POOL_SIZE,
)


#先创建 Engine；SQLAlchemy 默认惰性连接，不会在启动时立刻连库
engine = create_engine(
    DATABASE_URL,
    pool_size=DB_POOL_SIZE,
    max_overflow=DB_MAX_OVERFLOW,
    pool_recycle=DB_POOL_RECYCLE,
    pool_pre_ping=DB_POOL_PRE_PING,
)   

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Generator[Session, None, None]:
    # 每个请求拿一个会话，请求结束后关闭， 避免连接泄漏
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()