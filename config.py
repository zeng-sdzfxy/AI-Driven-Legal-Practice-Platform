"""
共享配置模块 - 所有后端服务从此导入配置

用法：
    from config import settings, get_db_url, hash_password, verify_password, create_access_token, verify_token
"""
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from passlib.context import CryptContext
from jose import JWTError, jwt

# 自动加载 .env 文件
load_dotenv()

# bcrypt 密码上下文（全局单例）
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Settings:
    """应用配置，所有值从环境变量读取，带默认回退"""

    # 阿里云 DashScope
    DASHSCOPE_API_KEY: str = os.getenv("DASHSCOPE_API_KEY", "")

    # 数据库
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_NAME: str = os.getenv("DB_NAME", "rbac_system")

    # JWT
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "rbac-system-2025-secure-key")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", "30"))

    # 服务端口
    RBAC_SERVICE_PORT: int = int(os.getenv("RBAC_SERVICE_PORT", "8001"))
    MAIN_SERVICE_PORT: int = int(os.getenv("MAIN_SERVICE_PORT", "8000"))
    TASK_SERVICE_PORT: int = int(os.getenv("TASK_SERVICE_PORT", "8002"))
    COURT_SERVICE_PORT: int = int(os.getenv("COURT_SERVICE_PORT", "8003"))
    CASE_SERVICE_PORT: int = int(os.getenv("CASE_SERVICE_PORT", "8004"))

    # CORS
    @property
    def CORS_ORIGINS(self) -> list[str]:
        origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
        return [o.strip() for o in origins.split(",") if o.strip()]


settings = Settings()


def get_db_url(database: str | None = None) -> str:
    """构建 MySQL 数据库连接 URL"""
    db = database or settings.DB_NAME
    return f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{db}"


def hash_password(password: str) -> str:
    """对密码进行 bcrypt 哈希"""
    return _pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码

    过渡方案：先尝试 bcrypt 验证，失败后回退明文比对。
    明文回退仅在旧数据迁移期间使用，后续应移除。
    """
    try:
        return _pwd_context.verify(plain_password, hashed_password)
    except ValueError:
        # 哈希格式不是 bcrypt（旧明文密码），回退明文比对
        # TODO: 迁移完所有用户后移除此回退
        return plain_password == hashed_password


def create_access_token(data: dict) -> str:
    """创建 JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def verify_token(token: str) -> dict | None:
    """验证 JWT token，成功返回 payload 字典，失败返回 None"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None
