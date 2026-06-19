from sqlalchemy import Column, String, Text, DateTime, Integer, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from pydantic import BaseModel
from fastapi import FastAPI, APIRouter, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import hashlib
import json

from config import settings, get_db_url, verify_token

# 初始化数据库连接
Base = declarative_base()

# 数据库引擎配置（从环境变量读取）
DATABASE_URL = get_db_url()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 1. 案件信息表模型
class Case(Base):
    """案件信息表"""
    __tablename__ = "cases"

    id = Column(String(50), primary_key=True, comment="案件唯一标识")
    theme = Column(String(100), nullable=False, comment="案件类型")
    plaintiff_name = Column(String(100), nullable=False, comment="原告姓名/名称")
    plaintiff_contact = Column(String(100), comment="原告联系方式")
    plaintiff_address = Column(String(200), comment="原告地址")
    defendant_name = Column(String(100), nullable=False, comment="被告姓名/名称")
    defendant_contact = Column(String(100), comment="被告联系方式")
    defendant_address = Column(String(200), comment="被告地址")
    details = Column(Text, nullable=False, comment="案件事实与经过")
    evidence = Column(Text, comment="证据材料")
    claims = Column(Text, nullable=False, comment="诉讼请求")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")

    # 关联对话记录
    dialogues = relationship("DialogueRecord", backref="case", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Case(id='{self.id}', theme='{self.theme}')>"

# 2. 评价报告表模型
class Evaluation(Base):
    """评价报告表"""
    __tablename__ = "evaluations"

    id = Column(String(50), primary_key=True, comment="评价报告ID")
    case_id = Column(String(50), nullable=False, comment="关联的案件ID")
    topic = Column(String(100), nullable=False, comment="案件类型")
    role = Column(String(50), nullable=False, comment="用户角色")
    time = Column(DateTime, default=datetime.now, comment="评价时间")
    summary = Column(Text, comment="对话总结")
    professional = Column(Integer, comment="法律专业性评分")
    logic = Column(Integer, comment="逻辑清晰度评分")
    evidence = Column(Integer, comment="证据运用评分")
    expression = Column(Integer, comment="表达流畅度评分")
    adaptation = Column(Integer, comment="角色适应性评分")
    total_score = Column(Integer, comment="综合评分")
    strengths = Column(Text, comment="优点（JSON字符串）")
    improvements = Column(Text, comment="改进点（JSON字符串）")
    comments = Column(Text, comment="专业点评")

    def __repr__(self):
        return f"<Evaluation(id='{self.id}', case_id='{self.case_id}')>"

# 3. 新增对话记录表模型
class DialogueRecord(Base):
    """法庭对话记录表"""
    __tablename__ = "dialogue_records"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="发言顺序（自增ID）")
    content = Column(Text, nullable=False, comment="发言内容")
    speaker = Column(String(50), nullable=False, comment="发言人物（原告/被告/法官/原告律师/被告律师）")
    case_type = Column(String(100), nullable=False, comment="案件类型")
    case_id = Column(String(50), ForeignKey("cases.id"), nullable=False, comment="关联的案件ID")
    create_time = Column(DateTime, default=datetime.now, comment="发言时间")

    def __repr__(self):
        return f"<DialogueRecord(id={self.id}, speaker='{self.speaker}', case_id='{self.case_id}')>"

# 4. Pydantic模型（请求/响应数据验证）
class CaseCreate(BaseModel):
    """创建案件的请求数据模型"""
    id: str
    theme: str
    plaintiff: dict  # {name, contact, address}
    defendant: dict  # {name, contact, address}
    details: str
    evidence: str = ""
    claims: str
    created_at: str = ""

class EvaluationCreate(BaseModel):
    """创建评价报告的请求数据模型"""
    case_id: str
    topic: str
    role: str
    summary: str
    professional: int
    logic: int
    evidence: int
    expression: int
    adaptation: int
    total_score: int
    strength: str  # JSON字符串
    improvements: str  # JSON字符串
    comments: str

class DialogueCreate(BaseModel):
    """创建对话记录的请求模型"""
    content: str
    speaker: str
    case_type: str
    case_id: str

# 5. 依赖项：获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 6. FastAPI 应用初始化
app = FastAPI(title="案件与对话管理服务")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 认证依赖：验证请求中的 JWT token
def verify_case_auth(authorization: str = Header(None)):
    """对所有写操作进行 JWT 认证"""
    if not authorization:
        raise HTTPException(status_code=401, detail="未提供认证令牌")
    token = authorization.replace("Bearer ", "")
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="无效的认证令牌")
    return payload

# 7. 接口路由初始化
router = APIRouter()

# 8. 案件相关接口
@router.post("/api/cases", response_model=dict)
def create_case(case: CaseCreate, db: Session = Depends(get_db), current_user: dict = Depends(verify_case_auth)):
    """保存案件信息到数据库（需认证）"""
    if not case.plaintiff.get("name") or not case.defendant.get("name"):
        raise HTTPException(status_code=400, detail="原告和被告姓名为必填项")
    
    db_case = Case(
        id=case.id,
        theme=case.theme,
        plaintiff_name=case.plaintiff.get("name", ""),
        plaintiff_contact=case.plaintiff.get("contact", ""),
        plaintiff_address=case.plaintiff.get("address", ""),
        defendant_name=case.defendant.get("name", ""),
        defendant_contact=case.defendant.get("contact", ""),
        defendant_address=case.defendant.get("address", ""),
        details=case.details,
        evidence=case.evidence,
        claims=case.claims
    )
    try:
        db.add(db_case)
        db.commit()
        db.refresh(db_case)
        return {"message": "案件保存成功", "case_id": db_case.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"保存失败：{str(e)}")

@router.get("/api/cases/{case_id}", response_model=dict)
def get_case(case_id: str, db: Session = Depends(get_db)):
    """查询案件信息"""
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="案件不存在")
    return {
        "id": case.id,
        "theme": case.theme,
        "plaintiff": {
            "name": case.plaintiff_name,
            "contact": case.plaintiff_contact,
            "address": case.plaintiff_address
        },
        "defendant": {
            "name": case.defendant_name,
            "contact": case.defendant_contact,
            "address": case.defendant_address
        },
        "details": case.details,
        "evidence": case.evidence,
        "claims": case.claims,
        "created_at": case.created_at.strftime("%Y-%m-%d %H:%M:%S")
    }

# 8. 评价报告相关接口
@router.post("/evaluate", response_model=dict)
def create_evaluation(eval_data: EvaluationCreate, db: Session = Depends(get_db), current_user: dict = Depends(verify_case_auth)):
    """保存评价报告到数据库（需认证）"""
    hash_obj = hashlib.md5(f"{eval_data.case_id}{datetime.now()}".encode())
    eval_id = f"eval_{hash_obj.hexdigest()[:12]}"
    
    db_eval = Evaluation(
        id=eval_id,
        case_id=eval_data.case_id,
        topic=eval_data.topic,
        role=eval_data.role,
        summary=eval_data.summary,
        professional=eval_data.professional,
        logic=eval_data.logic,
        evidence=eval_data.evidence,
        expression=eval_data.expression,
        adaptation=eval_data.adaptation,
        total_score=eval_data.total_score,
        strength=eval_data.strength,
        improvements=eval_data.improvements,
        comments=eval_data.comments
    )
    
    try:
        db.add(db_eval)
        db.commit()
        db.refresh(db_eval)
        return {"message": "评价报告保存成功", "id": db_eval.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"评价保存失败：{str(e)}")

# 9. 新增对话记录相关接口
@router.post("/api/dialogues", response_model=dict)
def save_dialogue(dialogue: DialogueCreate, db: Session = Depends(get_db), current_user: dict = Depends(verify_case_auth)):
    """保存单条对话记录（需认证）"""
    # 验证发言人物合法性
    valid_speakers = ["原告", "被告", "法官", "原告律师", "被告律师"]
    if dialogue.speaker not in valid_speakers:
        raise HTTPException(status_code=400, detail=f"无效的发言人物：{dialogue.speaker}，允许的值：{valid_speakers}")
    
    # 验证案件是否存在
    case = db.query(Case).filter(Case.id == dialogue.case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail=f"案件ID不存在：{dialogue.case_id}")
    
    # 创建数据库记录
    db_dialogue = DialogueRecord(
        content=dialogue.content,
        speaker=dialogue.speaker,
        case_type=dialogue.case_type,
        case_id=dialogue.case_id
    )
    
    try:
        db.add(db_dialogue)
        db.commit()
        db.refresh(db_dialogue)
        return {
            "message": "对话记录保存成功",
            "dialogue_id": db_dialogue.id  # 返回发言顺序ID
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"保存对话失败：{str(e)}")

@router.get("/api/cases/{case_id}/dialogues", response_model=list)
def get_case_dialogues(case_id: str, db: Session = Depends(get_db)):
    """获取指定案件的所有对话记录"""
    dialogues = db.query(DialogueRecord)\
                  .filter(DialogueRecord.case_id == case_id)\
                  .order_by(DialogueRecord.id)\
                  .all()
    
    if not dialogues:
        return []
    
    return [
        {
            "id": d.id,
            "content": d.content,
            "speaker": d.speaker,
            "case_type": d.case_type,
            "create_time": d.create_time.strftime("%Y-%m-%d %H:%M:%S")
        } for d in dialogues
    ]

# 挂载路由
app.include_router(router)

# 初始化数据库表
def init_db():
    Base.metadata.create_all(bind=engine)
    print("数据库表初始化完成")

if __name__ == "__main__":
    import uvicorn
    init_db()
    uvicorn.run("case_model:app", host="0.0.0.0", port=settings.CASE_SERVICE_PORT, reload=True)