from passlib.context import CryptContext
from datetime import datetime, timedelta, UTC
from jose import jwt, JWTError
from app.core.config import JWT_ACCESS_TOKEN_EXPIRE_MINUTES, JWT_SECRET_KEY, JWT_ALGORITHM

# 使用 bcrypt 作为当前密码哈希方案 （可后续平滑升级）
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    # 注册时把明文转成哈希
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # 登录时调用：校验明文是否匹配已存储哈希
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(subject: str) -> str:
    expire_at = datetime.now(UTC) + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": subject,
        "exp": expire_at,
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    # 只负责解码与验签： 业务层再决定如何处理sub缺失等问题
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError as exc:
        raise ValueError("Invalid token") from exc