import os


# 配置先用环境变量读取；后续会升级到 .env +分环境配置
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://todo_user:todo_pass@127.0.0.1:3306/todo_db",
)


# 连接池关键参数：后续在 docker也会映射成环境变量
DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "5"))
DB_MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "10"))
DB_POOL_RECYCLE = int(os.getenv("DB_POOL_RECYCLE", "1800"))  # 30 分钟
DB_POOL_PRE_PING = os.getenv("DB_POOL_PRE_PING", "true").lower() == "true"

# JWT
# JWT
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-change-me")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30")
)
