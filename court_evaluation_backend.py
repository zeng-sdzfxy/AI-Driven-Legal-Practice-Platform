from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import mysql.connector
from mysql.connector import errorcode
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Generator, List
import json
from typing import Optional

from config import settings, get_db_url, verify_token


# 数据库配置（从环境变量读取，与 rbac_auth 共享）
DB_CONFIG = {
    "host": settings.DB_HOST,
    "user": settings.DB_USER,
    "password": settings.DB_PASSWORD,
    "database": settings.DB_NAME
}

# 初始化FastAPI应用并添加CORS中间件
app = FastAPI(title="模拟法庭评价报告服务")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据库连接和初始化
def init_db():
    cnx = mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"]
    )
    cursor = cnx.cursor()
    
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        print(f"[OK] Database '{DB_CONFIG['database']}' created/exists")
    except mysql.connector.Error as err:
        print(f"[ERROR] Create database failed: {err}")
        return None
    
    cursor.close()
    cnx.close()
    
    DATABASE_URL = get_db_url()
    engine = create_engine(DATABASE_URL)
    
    Base.metadata.create_all(bind=engine)
    
    return engine

# 导入或定义User模型
try:
    from rbac_auth import Base, User
    print("[OK] Successfully imported rbac_auth dependency")
except ImportError:
    print("[WARN] Cannot import rbac_auth, using local fallback model")
    Base = declarative_base()
    
    class User(Base):
        __tablename__ = "users"
        username = Column(String(50), primary_key=True, index=True)
        password = Column(String(256), nullable=False)
        role = Column(String(50), nullable=False)

# 定义评价报告模型 - 包含案件关联字段
class CourtEvaluationReport(Base):
    __tablename__ = "court_evaluation_reports"
    
    # 主键ID
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # 关联用户表的username（外键）
    username = Column(String(50), ForeignKey("users.username"), nullable=False)
    
    # 新增：案件ID关联（与前端caseInfo.id对应）
    case_id = Column(String(50), nullable=False, index=True)  # 案件唯一标识
    
    # 前端所需的所有字段
    topic = Column(String(200), nullable=False)  # 主题（冗余字段，便于快速查看）
    role = Column(String(50), nullable=False)    # 角色
    time = Column(DateTime, nullable=False)      # 时间
    summary = Column(Text, nullable=False)       # 对话摘要
    
    # 分项评分
    professional = Column(Float, nullable=False)  # 法律专业性
    logic = Column(Float, nullable=False)         # 逻辑清晰度
    evidence = Column(Float, nullable=False)      # 证据运用
    expression = Column(Float, nullable=False)    # 表达流畅度
    adaptation = Column(Float, nullable=False)    # 角色适应性
    
    total_score = Column(Float, nullable=False)   # 总评分
    strengths = Column(Text, nullable=False)      # 优点分析（JSON字符串）
    improvements = Column(Text, nullable=False)   # 改进建议（JSON字符串）
    comments = Column(Text, nullable=False)       # 专业点评
    
    create_time = Column(DateTime, default=datetime.now)  # 创建时间
    
    # 与用户表的关系
    user = relationship("User", backref="court_evaluations")

# 初始化数据库
engine = init_db()
if engine:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    print("[OK] court service: database initialized")
else:
    print("[ERROR] court service: database initialization failed")

# 依赖项：获取数据库会话
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 依赖项：获取当前用户
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8001/rbac/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

# Pydantic模型：评价报告相关
class ReportBase(BaseModel):
    case_id: str  # 案件ID
    topic: str
    role: str
    time: datetime
    summary: str
    professional: float
    logic: float
    evidence: float
    expression: float
    adaptation: float
    total_score: float
    strengths: str
    improvements: str
    comments: str

class ReportCreate(ReportBase):
    pass

class Report(ReportBase):
    id: int
    username: str
    create_time: datetime
    
    class Config:
        orm_mode = True

# API路由：评价报告相关
@app.post("/api/evaluation", response_model=Report)
def create_report(report: ReportCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """创建新的评价报告（包含案件ID关联）"""
    if current_user.role != "模拟法庭":
        raise HTTPException(status_code=403, detail="权限不足：只有模拟法庭角色可以创建评价报告")
    
    db_report = CourtEvaluationReport(
        **report.dict(),
        username=current_user.username
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

@app.get("/api/evaluation", response_model=List[Report])
def read_reports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """获取评价报告列表"""
    if current_user.role != "模拟法庭":
        raise HTTPException(status_code=403, detail="权限不足：只有模拟法庭角色可以查看评价报告")
    
    # 管理员可以查看所有记录，普通用户只能查看自己的
    if current_user.role == "管理员":
        reports = db.query(CourtEvaluationReport).offset(skip).limit(limit).all()
    else:
        reports = db.query(CourtEvaluationReport)\
                    .filter(CourtEvaluationReport.username == current_user.username)\
                    .offset(skip)\
                    .limit(limit)\
                    .all()
    return reports

@app.get("/api/evaluation/{report_id}", response_model=Report)
def read_report(report_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """获取指定ID的评价报告"""
    if current_user.role != "模拟法庭":
        raise HTTPException(status_code=403, detail="权限不足：只有模拟法庭角色可以查看评价报告")
    
    report = db.query(CourtEvaluationReport).filter(CourtEvaluationReport.id == report_id).first()
    if report is None:
        raise HTTPException(status_code=404, detail="评价报告不存在")
    
    # 权限检查：管理员可以查看所有，普通用户只能查看自己的
    if report.username != current_user.username and current_user.role != "管理员":
        raise HTTPException(status_code=403, detail="权限不足：只能查看自己创建的报告")
    
    return report

@app.get("/api/evaluation/case/{case_id}", response_model=List[Report])
def read_reports_by_case(
    case_id: str, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """根据案件ID查询关联的评价报告"""
    if current_user.role != "模拟法庭":
        raise HTTPException(status_code=403, detail="权限不足：只有模拟法庭角色可以查看评价报告")
    
    # 基础查询
    query = db.query(CourtEvaluationReport)\
              .filter(CourtEvaluationReport.case_id == case_id)
    
    # 权限过滤：普通用户只能查看自己的
    if current_user.role != "管理员":
        query = query.filter(CourtEvaluationReport.username == current_user.username)
    
    reports = query.order_by(CourtEvaluationReport.create_time.desc()).all()
    
    if not reports:
        raise HTTPException(status_code=404, detail=f"该案件（ID: {case_id}）暂无评价报告")
    
    return reports

"""按条件查询评价报告"""
@app.get("/api/evaluation/search", response_model=List[Report])
def search_reports(
    case_id: Optional[str] = None,
    topic: Optional[str] = None,
    min_score: Optional[float] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """按条件查询评价报告"""
    if current_user.role != "模拟法庭":
        raise HTTPException(status_code=403, detail="权限不足：只有模拟法庭角色可以查看评价报告")
    
    query = db.query(CourtEvaluationReport)
    
    # 普通用户只能查看自己的报告
    if current_user.role != "管理员":
        query = query.filter(CourtEvaluationReport.username == current_user.username)
    
    # 应用筛选条件
    if case_id:
        query = query.filter(CourtEvaluationReport.case_id == case_id)
    if topic:
        query = query.filter(CourtEvaluationReport.topic.like(f"%{topic}%"))
    if min_score is not None:
        query = query.filter(CourtEvaluationReport.total_score >= min_score)
    if start_date:
        query = query.filter(CourtEvaluationReport.create_time >= start_date)
    if end_date:
        query = query.filter(CourtEvaluationReport.create_time <= end_date)
    
    reports = query.offset(skip).limit(limit).all()
    return reports

@app.delete("/api/evaluation/{report_id}")
def delete_report(report_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """删除指定ID的评价报告"""
    if current_user.role not in ["模拟法庭", "管理员"]:
        raise HTTPException(status_code=403, detail="权限不足：只有模拟法庭角色或管理员可以删除评价报告")
    
    report = db.query(CourtEvaluationReport).filter(CourtEvaluationReport.id == report_id).first()
    if report is None:
        raise HTTPException(status_code=404, detail="评价报告不存在")
    
    if report.username != current_user.username and current_user.role != "管理员":
        raise HTTPException(status_code=403, detail="权限不足：只能删除自己创建的报告")
    
    db.delete(report)
    db.commit()
    return {"detail": "评价报告已成功删除"}

if __name__ == "__main__":
    import uvicorn
    print("[INFO] Starting court evaluation report service...")
    uvicorn.run(app, host="0.0.0.0", port=8003)