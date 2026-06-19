import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import declarative_base
from datetime import datetime
import mysql.connector
from mysql.connector import errorcode
import traceback

from config import settings, get_db_url, hash_password, verify_password, create_access_token, verify_token
# --------------------------
# 1. 数据库基础配置
# --------------------------
# 数据库配置（从环境变量读取）
DB_CONFIG = {
    "user": settings.DB_USER,
    "password": settings.DB_PASSWORD,
    "host": settings.DB_HOST,
    "database": settings.DB_NAME
}

# 自动创建数据库
try:
    conn = mysql.connector.connect(
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        host=DB_CONFIG["host"],
        connect_timeout=10
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
    cursor.close()
    conn.close()
    print(f"[OK] Database '{DB_CONFIG['database']}' created/exists")
except mysql.connector.Error as err:
    print(f"[ERROR] Database connection failed: {str(err)}")
    exit()

# 创建数据库引擎
DATABASE_URL = get_db_url()
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_recycle=300
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 基类
Base = declarative_base()

# --------------------------
# 2. 数据表（3列：账号/密码/身份）
# --------------------------
class User(Base):
    __tablename__ = "users"
    username = Column(String(50), primary_key=True, nullable=False)  # 账号（主键，唯一）
    password = Column(String(256), nullable=False)                  # 密码（bcrypt 哈希）
    role = Column(String(50), nullable=False)                      # 身份

# 创建表
try:
    Base.metadata.create_all(bind=engine)
    print("[OK] Table 'users' created/exists")
except Exception as e:
    print(f"[ERROR] Table creation failed: {str(e)}")
    exit()

# --------------------------
# 3. Pydantic模型（新增注册模型）
# --------------------------
class UserLogin(BaseModel):
    username: str
    password: str

class UserRegister(BaseModel):
    """注册用模型：包含用户名、密码、角色"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名长度3-50")
    password: str = Field(..., min_length=6, description="密码至少6位")
    role: str = Field(..., description="必须是：模拟法庭/敏感数据/任务管理系统")

class UserResponse(BaseModel):
    username: str
    role: str
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    username: str
    role: str

class TokenData(BaseModel):
    username: str | None = None
    role: str | None = None

# --------------------------
# 4. JWT配置
# --------------------------
# --------------------------
# 5. 工具函数
# --------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def _verify_token_or_raise(token: str, credentials_exception):
    """验证 JWT token，失败时抛出异常；成功返回 TokenData"""
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception
    username: str = payload.get("sub")
    role: str = payload.get("role")
    if username is None or role is None:
        raise credentials_exception
    return TokenData(username=username, role=role)

# --------------------------
# 6. 自动创建默认账号
# --------------------------
def auto_create_default_users():
    try:
        db = SessionLocal()
        default_users = [
            {"username": "court_user", "password": "Court123456", "role": "模拟法庭"},
            {"username": "data_admin", "password": "Data123456", "role": "敏感数据"},
            {"username": "task_admin", "password": "Task123456", "role": "任务管理系统"}
        ]
        created_users = []
        exist_users = []
        
        for user_info in default_users:
            existing_user = db.query(User).filter(User.username == user_info["username"]).first()
            if existing_user:
                exist_users.append(user_info["username"])
                continue
            new_user = User(
                username=user_info["username"],
                password=hash_password(user_info["password"]),
                role=user_info["role"]
            )
            db.add(new_user)
            created_users.append(user_info["username"])
        
        db.commit()
        if created_users:
            print(f"[OK] Auto-created default users: {created_users}")
        if exist_users:
            print(f"[INFO] Default users already exist: {exist_users}")
        db.close()
    except Exception as e:
        print(f"[ERROR] Auto-create default users failed: {str(e)}")

# --------------------------
# 7. 带/rbac前缀的路由（新增注册接口）
# --------------------------
rbac_router = APIRouter(prefix="/rbac")

# 健康检查
@rbac_router.get("/health")
def health_check():
    return {"status": "ok", "port": 8001, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

# 登录接口
@rbac_router.post("/auth/login", response_model=Token)
def login(
    user_login: UserLogin,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == user_login.username).first()
    if not user:
        raise HTTPException(status_code=401, detail=f"账号 '{user_login.username}' 不存在")
    if not verify_password(user_login.password, user.password):
        raise HTTPException(status_code=401, detail="密码错误")
    
    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username,
        "role": user.role
    }

# 新增：注册接口（解决404问题）
@rbac_router.post("/auth/register", response_model=UserResponse)
def register(
    user_register: UserRegister,
    db: Session = Depends(get_db)
):
    # 1. 验证角色是否合法
    allowed_roles = ["模拟法庭", "敏感数据", "任务管理系统"]
    if user_register.role not in allowed_roles:
        raise HTTPException(
            status_code=400,
            detail=f"角色必须是以下之一：{allowed_roles}"
        )
    
    # 2. 检查用户名是否已存在
    existing_user = db.query(User).filter(User.username == user_register.username).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail=f"用户名 '{user_register.username}' 已被注册"
        )
    
    # 3. 创建新用户（密码哈希存储）
    new_user = User(
        username=user_register.username,
        password=hash_password(user_register.password),
        role=user_register.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # 刷新数据，确保返回最新状态
    
    print(f"[OK] User registered: {user_register.username} (role: {user_register.role})")
    return new_user

# Token验证接口
@rbac_router.post("/auth/verify-token")
def verify_user_token(token: str, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=401, detail="令牌无效/已过期")
    token_data = _verify_token_or_raise(token, credentials_exception)
    user = db.query(User).filter(User.username == token_data.username).first()
    if not user:
        raise credentials_exception
    return {"username": user.username, "role": user.role, "valid": True}

# --------------------------
# 8. FastAPI应用实例
# --------------------------
app = FastAPI(title="RBAC权限服务（带注册功能）", version="1.0")

# 跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rbac_router)

# --------------------------
# 9. 启动服务
# --------------------------
if __name__ == "__main__":
    auto_create_default_users()
    uvicorn.run(
        "rbac_auth:app",
        host="0.0.0.0",
        port=8001,
        reload=False,  # 稳定模式
        workers=1
    )
