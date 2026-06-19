from fastapi import FastAPI, Request, HTTPException, Depends, status
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
import openai
import os
import json
import re
from typing import Dict, Any, List

from config import settings

# 导入数据库相关依赖和模型
from court_evaluation_backend import get_db, get_current_user, CourtEvaluationReport, User, ReportBase

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = openai.OpenAI(
    api_key=settings.DASHSCOPE_API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

session_context: Dict[str, Any] = {}

# 定义评价报告创建模型（与court_evaluation_backend.py保持一致）
class ReportCreate(ReportBase):
    pass

# 确定下一个发言人的API端点
@app.post("/api/determine-next-speaker")
async def determine_next_speaker(request: Request):
    """解析法官发言内容，确定下一个应该发言的角色（原告律师或被告律师）"""
    try:
        data = await request.json()
        judge_message = data.get("message", "")  # 法官的发言内容
        theme = data.get("theme", "")            # 案件主题
        history = data.get("history", [])        # 对话历史
        
        # 如果法官发言为空，默认返回原告律师
        if not judge_message.strip():
            return JSONResponse(content={"nextSpeaker": "原告律师"})
        
        # 构建系统提示词，指导AI如何判断下一个发言人
        system_prompt = """你是一个法庭流程分析助手，需要根据法官的发言内容判断下一个应该发言的是原告律师还是被告律师。
        请遵循以下规则：
        1. 如果法官明确提到原告、原告律师或直接向原告方提问，下一个发言人应为"原告律师"
        2. 如果法官明确提到被告、被告律师或直接向被告方提问，下一个发言人应为"被告律师"
        3. 如果法官只是陈述事实、法律条款或进行总结，且没有明确指向，根据法庭惯例交替发言
        4. 初始阶段如果没有明确指向，默认先由原告律师发言
        5. 只返回"原告律师"或"被告律师"，不要添加任何额外内容
        
        请基于上述规则，仅根据法官的发言内容判断下一个发言人。"""
        
        # 构建用户提示，包含法官发言和案件背景
        user_prompt = f"""案件主题：{theme}
        法官发言：{judge_message}
        
        请判断下一个应该发言的是原告律师还是被告律师？只返回角色名称，不要添加其他内容。"""
        
        # 调用AI模型进行判断
        response = client.chat.completions.create(
            model="qwen-plus-2025-07-14",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,  # 降低随机性，确保判断更稳定
            max_tokens=10
        )
        
        # 提取并处理AI返回的结果
        result = response.choices[0].message.content.strip()
        
        # 验证结果是否有效，无效则使用默认逻辑
        if result not in ["原告律师", "被告律师"]:
            # fallback逻辑：根据历史记录判断谁是上一个发言的非法官角色
            non_judge_speakers = [msg for msg in history if msg.get("role") in ["原告律师", "被告律师"]]
            if non_judge_speakers:
                last_speaker = non_judge_speakers[-1]["role"]
                # 交替发言
                result = "被告律师" if last_speaker == "原告律师" else "原告律师"
            else:
                # 没有历史记录时默认原告律师先发言
                result = "原告律师"
        
        return JSONResponse(content={"nextSpeaker": result})
        
    except Exception as e:
        print(f"判断下一个发言人时出错: {str(e)}")
        # 出错时默认返回原告律师
        return JSONResponse(content={"nextSpeaker": "原告律师"})

@app.post("/api/chat")
async def chat_endpoint(request: Request):
    data = await request.json()
    role = data["role"]
    theme = data["theme"]
    history = data["history"]

    # 根据角色构建不同的系统提示
    if role == "法官":
        system_prompt = f"""你是一名专业的法官，正在主持一场模拟法庭审理，案件主题为{theme}。
        请严格遵循以下流程，灵活运用法律条文，确保审理程序合法合规，尊重当事人的合法权益。
        1. 庭审开场
        "尊敬的原告、被告及旁听人员，欢迎参与本次模拟法庭。我是本案的AI法官，将主持庭审并依法作出公正裁决。现在，庭审正式开始。首先，请原告方陈述诉讼请求、事实及理由。"
        2. 原告陈述后
        "感谢原告的陈述。接下来，请被告方针对原告的主张进行答辩，并提供相关证据或解释。"
        3. 被告答辩后
        "感谢双方当事人的陈述。根据现有陈述，本庭需要进一步澄清以下问题：
        - 原告提及的[具体问题1]，请提供更多细节或证据支持；
        - 被告主张的[具体反驳1]，请说明依据及来源。"
        4. 证据审查
        "双方已完成主要事实陈述。现在进入证据审查环节：
        - 原告提交的[证据名称1]，请说明其来源、关联性及证明目的；
        - 被告对该证据有何异议或补充？"
        5. 法律分析与初步意见
        "基于双方陈述及证据，本庭将依据《中华人民共和国民法典》[具体条款]进行法律分析。
        特别关注[争议焦点]，请双方进一步阐述观点：
        - 原告方是否有新的事实或理由需要补充？
        - 被告方对该法律适用有何异议？"
        6. 补充提问与确认
        "经审查，本庭需要确认以下事项：
        - [具体问题2]，请原告方明确答复；
        - [具体问题3]，请被告方提供依据。"
        7. 休庭或闭庭宣布
        "感谢双方当事人的充分陈述与辩论。本庭将综合全案证据及法律规定，依法作出裁决。
        （若需进一步调查或评议）现宣布休庭，择期继续审理。
        （若审理完毕）现宣布闭庭，本案判决结果如下：[判决结果]。"
        """
    elif role == "原告律师":
        system_prompt = f"""你是一个专业的律师，代表原告方，正在进行模拟法庭审理，案件主题是{theme}。
        以下是对本角色的要求：请直接陈述要点，不要使用任何标题，如案件背景梳理、法律依据阐述等。在民事诉讼中，并不存在 “陪审团”，我国民事案件的审判组织形式主要是独任制和合议制，由法官或法官与人民陪审员组成合议庭进行审理。请结合案件事实，引用具体的法律条文支持主张，列出准备提交的所有证据，明确诉讼请求，并详细阐述支持诉讼请求的理由。 \n"""
    elif role == "被告律师":
        system_prompt = f"""你是一个专业的律师，代表被告方，正在进行模拟法庭审理，案件主题是{theme}。
        请严格遵循以下要求：用第一人称我，以被告律师的角度进行辩护，应称呼被告为我的当事人。提出辩护意见，反驳控方指控。引用相关法律条文反驳原告论点，分析证据证人的不合法性，抓住漏洞提出质疑，并提出异议。直接陈述要点，条理清晰，不要重复角色名称。\n"""
    else:
        raise HTTPException(status_code=400, detail="未知的角色")

    history_prompt = "\n".join([f"{msg['type']}: {msg['content']}" for msg in history[-6:]])  # 保留最近6条历史
    full_prompt = system_prompt + history_prompt + "\n请生成符合当前角色身份的下一句发言："

    try:
        completion = client.chat.completions.create(
            model="qwen-plus-2025-07-14",
            messages=[{
                "role": "system",
                "content": system_prompt
            }, {
                "role": "user",
                "content": full_prompt
            }],
            stream=True,
            temperature=0.7,
            max_tokens=1000
        )

        async def generate():
            full_response = ""
            for chunk in completion:
                if chunk.choices:
                    delta = chunk.choices[0].delta
                    if hasattr(delta, "content"):
                        content = delta.content
                        full_response += content
                        yield f"data: {json.dumps({'content': content})}\n\n"
            yield "data: [DONE]\n\n"

            # 更新对话历史
            session_id = request.client.host
            if session_id not in session_context:
                session_context[session_id] = {"history": []}
            session_context[session_id]["history"].append({
                "role": role,
                "content": full_response,
                "type": "ai"
            })

        return StreamingResponse(generate(), media_type="text/event-stream")

    except Exception as e:
        print(f"API调用失败: {str(e)}")
        async def error_stream():
            yield f"data: {json.dumps({'content': '(系统错误，请重试)'} )}\n\n"
            yield "data: [DONE]\n\n"
        return StreamingResponse(error_stream(), media_type="text/event-stream")

@app.post("/evaluate")
async def evaluate_conversation(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """生成专业的对话评价报告并存储到数据库"""
    try:
        # 检查用户权限
        if current_user.role != "模拟法庭":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足：只有模拟法庭角色可以生成评价报告"
            )
            
        data = await request.json()
        theme = data.get("theme", "")
        user_role = data.get("userRole", "")
        case_id = data.get("case_id")  # 新增：获取案件ID
        conversation_history = data.get("conversationHistory", [])
        user_contributions = data.get("userContributions", [])
        if not case_id:
            raise HTTPException(status_code=400, detail="缺少必填字段：case_id")

        
        
        # 构建评价提示词
        system_prompt = f"""你是一位资深的法律教育专家，擅长对模拟法庭表现进行专业评价。
        请基于用户在模拟法庭中的表现，从法律专业性、逻辑清晰度、证据运用、表达流畅度和角色适应性五个维度进行评分（每项0-100分），
        并计算综合得分。同时提供详细的优点分析、改进建议和专业点评。
        
        评价对象角色为：{user_role}
        案件主题为：{theme}
        
        评分标准：
        1. 法律专业性：法律术语使用准确性、法律条文引用恰当性、法律逻辑正确性
        2. 逻辑清晰度：论点明确性、论证连贯性、逻辑严密性
        3. 证据运用：证据相关性、证据充分性、证据引用恰当性
        4. 表达流畅度：语言表达准确性、表达流畅性、专业术语使用
        5. 角色适应性：角色理解准确性、行为符合角色身份程度
        
        请严格以JSON格式返回评价结果，不要添加任何额外文本、解释或说明。JSON应包含以下字段：
        - summary: 对话内容摘要（300字以内）
        - overallScore: 综合评分（0-100）
        - categoryScores: 包含五个维度评分的对象，键为"法律专业性"、"逻辑清晰度"、"证据运用"、"表达流畅度"、"角色适应性"
        - strengths: 优点分析（列表形式，至少3点）
        - improvements: 改进建议（列表形式，至少3点）
        - professionalComment: 专业点评（500字左右）
        """
        
        # 准备用户发言内容
        user_contributions_text = "\n".join([f"发言 {i+1}: {content}" for i, content in enumerate(user_contributions)])
        
        # 准备对话历史摘要
        dialogue_summary = "\n".join([
            f"{msg['role']}: {msg['content'][:100]}{'...' if len(msg['content']) > 100 else ''}" 
            for msg in conversation_history[-10:]  # 取最近10条对话
        ])
        
        # 构建用户提示
        user_prompt = f"""以下是用户在模拟法庭中的发言内容：
{user_contributions_text}

以下是对话历史摘要：
{dialogue_summary}

请根据上述内容，按照要求的格式和评分标准进行评价。只返回JSON，不要添加其他内容。"""
        
        # 调用AI生成评价
        response = client.chat.completions.create(
            model="qwen-plus-2025-07-14",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.6,
            max_tokens=1500
        )
        
        # 提取并清理AI返回的内容
        evaluation_content = response.choices[0].message.content.strip()
        
        # 使用正则表达式提取JSON部分
        json_match = re.search(r'\{.*\}', evaluation_content, re.DOTALL)
        if json_match:
            evaluation_content = json_match.group(0)
        else:
            raise ValueError("无法从AI响应中提取JSON内容")
        
        # 解析JSON
        evaluation_json = json.loads(evaluation_content)
        
        # 验证评价结果格式并补充缺失的字段
        required_fields = ["summary", "overallScore", "categoryScores", "strengths", "improvements", "professionalComment"]
        for field in required_fields:
            if field not in evaluation_json:
                evaluation_json[field] = "" if field != "strengths" and field != "improvements" and field != "categoryScores" else [] if field != "categoryScores" else {}
        
        required_categories = ["法律专业性", "逻辑清晰度", "证据运用", "表达流畅度", "角色适应性"]
        for category in required_categories:
            if category not in evaluation_json["categoryScores"]:
                evaluation_json["categoryScores"][category] = 0
        
        # 确保评分在有效范围内
        evaluation_json["overallScore"] = max(0, min(100, int(evaluation_json["overallScore"])))
        for category in required_categories:
            evaluation_json["categoryScores"][category] = max(0, min(100, int(evaluation_json["categoryScores"][category])))
        
        # 存储评价报告到数据库
        report_data = ReportCreate(
            case_id=case_id,
            topic=theme,
            role=user_role,
            time=datetime.now(),
            summary=evaluation_json["summary"],
            professional=evaluation_json["categoryScores"]["法律专业性"],
            logic=evaluation_json["categoryScores"]["逻辑清晰度"],
            evidence=evaluation_json["categoryScores"]["证据运用"],
            expression=evaluation_json["categoryScores"]["表达流畅度"],
            adaptation=evaluation_json["categoryScores"]["角色适应性"],
            total_score=evaluation_json["overallScore"],
            strengths=json.dumps(evaluation_json["strengths"]),
            improvements=json.dumps(evaluation_json["improvements"]),
            comments=evaluation_json["professionalComment"]
        )
        
        # 创建数据库记录
        db_report = CourtEvaluationReport(
            **report_data.model_dump(),
            username=current_user.username
        )
        db.add(db_report)
        db.commit()
        db.refresh(db_report)
        
        # 在返回结果中添加报告ID
        evaluation_json["reportId"] = db_report.id
        
        return JSONResponse(content=evaluation_json)
        
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {str(e)}")
        print(f"错误的JSON内容: {evaluation_content if 'evaluation_content' in locals() else '未知'}")
        return JSONResponse(
            status_code=500,
            content={
                "summary": "评价生成失败：JSON格式错误",
                "overallScore": 0,
                "categoryScores": {
                    "法律专业性": 0,
                    "逻辑清晰度": 0,
                    "证据运用": 0,
                    "表达流畅度": 0,
                    "角色适应性": 0
                },
                "strengths": ["无法生成优点分析"],
                "improvements": ["无法生成改进建议"],
                "professionalComment": f"评价生成失败，解析JSON时出错: {str(e)}"
            }
        )
    except Exception as e:
        print(f"评价生成失败: {str(e)}")
        return JSONResponse(content={
            "summary": "评价生成过程中出现错误",
            "overallScore": 0,
            "categoryScores": {
                "法律专业性": 0,
                "逻辑清晰度": 0,
                "证据运用": 0,
                "表达流畅度": 0,
                "角色适应性": 0
            },
            "strengths": ["无法生成优点分析"],
            "improvements": ["无法生成改进建议"],
            "professionalComment": f"评价生成失败: {str(e)}"
        })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)