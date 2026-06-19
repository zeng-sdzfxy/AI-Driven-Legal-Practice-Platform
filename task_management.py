from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import declarative_base
from datetime import datetime
import requests

from config import settings, get_db_url

# 数据库配置 - 与RBAC系统使用同一个数据库
DATABASE_URL = get_db_url()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 数据模型 - 与RBAC系统的users表结构完全一致
class User(Base):
    __tablename__ = "users"  # 共用RBAC系统的用户表
    
    username = Column(String(50), primary_key=True, nullable=False)  # 与RBAC保持一致：username为主键
    password = Column(String(256), nullable=False)
    role = Column(String(50), nullable=False)

# Pydantic模型 - 修正配置项并匹配实际表结构
class UserResponse(BaseModel):
    username: str
    role: str
    
    class Config:
        from_attributes = True  # 替换orm_mode，适配Pydantic v2

# RBAC服务地址
RBAC_SERVICE_URL = f"http://localhost:{settings.RBAC_SERVICE_PORT}"

# 创建任务管理应用
app = FastAPI(title="任务管理系统", version="1.0")

# 跨域设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 验证令牌 - 调用RBAC服务验证
def verify_token(token: str):
    if not token:
        raise HTTPException(status_code=401, detail="未提供令牌")
    
    try:
        # 调用RBAC服务验证令牌
        response = requests.post(
            f"{RBAC_SERVICE_URL}/rbac/auth/verify-token",
            json={"token": token}
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="无效的令牌")
            
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"验证令牌时出错: {str(e)}")

# 角色验证依赖 - 仅允许任务管理角色访问
def require_task_role(token: str = Query(...)):
    user_data = verify_token(token)
    if user_data["role"] != "任务管理系统":
        raise HTTPException(
            status_code=403,
            detail="没有权限访问任务管理系统"
        )
    return user_data

# 根路由 - 验证登录状态并显示功能
@app.get("/")
def read_root(token: str = Query(None)):
    if not token:
        return {
            "message": "请先登录",
            "login_url": f"{RBAC_SERVICE_URL}/rbac/auth/login",
            "说明": "登录后使用令牌访问，例如: /users?token=你的令牌"
        }
    
    try:
        user_data = verify_token(token)
        return {
            "message": f"欢迎使用任务管理系统，{user_data['username']}",
            "可用接口": {
                "获取用户列表": "/users?token=你的令牌",
                "查看当前用户信息": "/current-user?token=你的令牌"
            }
        }
    except HTTPException:
        return {
            "message": "令牌无效或已过期",
            "login_url": f"{RBAC_SERVICE_URL}/rbac/auth/login"
        }

# 获取用户列表（仅任务管理员可访问）
@app.get("/users", response_model=list[UserResponse])
def get_users(
    skip: int = 0,
    limit: int = 20,
    current_user: dict = Depends(require_task_role),
    db: Session = Depends(get_db)
):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

# 获取当前登录用户信息
@app.get("/current-user", response_model=UserResponse)
def get_current_user(
    current_user: dict = Depends(require_task_role),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == current_user["username"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("task_management:app", host="0.0.0.0", port=8002, reload=True)  # 移除.py扩展名