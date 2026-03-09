from passlib.context import CryptContext

# 使用 bcrypt 作为当前密码哈希方案 （可后续平滑升级）
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    # 注册时把明文转成哈希
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # 登录时调用：校验明文是否匹配已存储哈希
    return pwd_context.verify(plain_password,hashed_password)