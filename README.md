# 🏛️ 模拟法庭 — AI 驱动的沉浸式法律实践平台

[![Vue](https://img.shields.io/badge/Vue-3.5-4FC08D?logo=vuedotjs)](https://vuejs.org/)
[![Vite](https://img.shields.io/badge/Vite-6.2-646CFF?logo=vite)](https://vitejs.dev/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python)](https://python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi)](https://fastapi.tiangolo.com/)

**模拟法庭** 是一个基于 AI 大模型的沉浸式法律实践平台。用户可以选择法官、原告律师、被告律师等角色，进入真实的法庭模拟场景，与 AI 驱动的其他角色进行多轮庭审对话。平台提供 **2D 对话模式** 和 **3D 沉浸式场景**，并在庭审结束后生成 **AI 多维评估报告**。

> 🎓 山东政法学院网络空间安全学院

---

## ✨ 功能亮点

| 功能 | 说明 |
|---|---|
| 🎭 **多角色扮演** | 自由选择法官、原告律师、被告律师，体验不同法律角色的思维与表达 |
| 🏟️ **2D / 3D 双模式** | 2D 对话专注内容，3D Unity 场景沉浸式还原真实法庭 |
| 🗣️ **语音输入** | 支持语音转文字和直接语音输入，贴近真实庭审 |
| 🤖 **AI 智能对话** | 基于阿里云通义千问大模型，自动生成各方角色的法律发言 |
| 📊 **多维评估报告** | AI 从法律专业性、逻辑清晰度、证据运用、表达流畅度等维度评分 |
| 📂 **案件管理** | 自定义案件信息、保存/加载案件、对话记录持久化 |
| 🔐 **JWT 认证鉴权** | 基于角色的访问控制（RBAC），支持多用户注册登录 |

---

## 📸 界面预览

> 💡 **截图说明**：请在 `screenshots/` 目录下放置您的截图，下方占位符会自动显示。

| 首页 Hero | 核心功能 |
|---|---|
| ![首页](./screenshots/home-hero.png) | ![功能](./screenshots/features.png) |

| 庭审流程 | 案例库 |
|---|---|
| ![流程](./screenshots/process.png) | ![案例](./screenshots/cases.png) |

| 2D 庭审对话 | 3D 法庭场景 |
|---|---|
| ![2D](./screenshots/chat-2d.png) | ![3D](./screenshots/chat-3d.png) |

| AI 评估报告 | 登录页面 |
|---|---|
| ![评估](./screenshots/evaluation.png) | ![登录](./screenshots/login.png) |

---

## 🛠️ 技术栈

### 前端
- **Vue 3** (Composition API + Options API) — 渐进式 JavaScript 框架
- **Vite 6** — 下一代前端构建工具
- **Vue Router 4** — 单页应用路由
- **Axios** — HTTP 请求库（JWT 拦截器）
- **Three.js** — 3D 法庭场景渲染
- **Unity WebGL** — 3D 沉浸式法庭体验
- **Font Awesome 6** — 图标库
- **CSS 自定义变量** — 红色法律主题设计系统

### 后端
- **Python FastAPI** — 高性能异步 Web 框架
- **MySQL** — 关系型数据库
- **JWT (HS256)** — 无状态身份认证
- **阿里云 DashScope** — 通义千问大模型 API（qwen-plus）
- **Uvicorn** — ASGI 服务器

### 微服务架构（5 个服务）

| 服务 | 文件 | 端口 | 职责 |
|---|---|---|---|
| 主对话服务 | `main.py` | 8000 | AI 对话流式响应、评估报告生成 |
| 认证服务 | `rbac_auth.py` | 8001 | 用户注册/登录、JWT 签发与验证 |
| 任务服务 | `task_management.py` | 8002 | 任务 CRUD |
| 庭审评估服务 | `court_evaluation_backend.py` | 8003 | 评估报告存储与查询 |
| 案件服务 | `case_model.py` | 8004 | 案件信息与对话记录管理 |

---

## 🚀 快速开始

### 环境要求

- **Node.js** >= 18
- **Python** >= 3.10
- **MySQL** >= 8.0

### 1. 克隆项目

```bash
git clone https://github.com/zeng-sdzfxy/AI-Driven-Legal-Practice-Platform.git
cd AI-Driven-Legal-Practice-Platform
```

### 2. 前端启动

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端默认运行在 `http://localhost:5173`

### 3. 后端启动

```bash
# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# 安装 Python 依赖
pip install fastapi uvicorn pymysql python-dotenv pyjwt

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入你的 API Key 和数据库密码

# 一键启动所有微服务
python start_services.py
```

后端服务默认运行在 `http://localhost:8000` ~ `8004`

### 4. 环境变量说明

复制 `.env.example` 为 `.env`，填写以下配置：

```bash
# DashScope AI API（阿里云通义千问）
DASHSCOPE_API_KEY=sk-your-api-key-here

# MySQL 数据库
DB_USER=root
DB_PASSWORD=your-database-password
DB_HOST=localhost
DB_NAME=rbac_system

# JWT 配置
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30

# 服务端口
MAIN_SERVICE_PORT=8000
RBAC_SERVICE_PORT=8001
TASK_SERVICE_PORT=8002
COURT_SERVICE_PORT=8003
CASE_SERVICE_PORT=8004

# CORS
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

> ⚠️ **注意**：`.env` 文件包含敏感信息，已被 `.gitignore` 排除，不会提交到 Git。

### 5. 初始化数据库

首次运行前，确保 MySQL 已启动并创建数据库：

```sql
CREATE DATABASE rbac_system DEFAULT CHARACTER SET utf8mb4;
```

后端服务启动时会自动创建所需的数据表。

---

## 📁 项目结构

```
AI-Driven-Legal-Practice-Platform/
├── index.html                    # Vite 入口 HTML
├── package.json                  # 前端依赖配置
├── vite.config.js                # Vite 构建配置
├── .env.example                  # 环境变量模板（可安全提交）
├── .env                          # 环境变量（已被 gitignore）
├── .gitignore                    # Git 忽略规则
├── .gitattributes                # Git LFS 配置
│
├── src/                          # 前端源代码
│   ├── main.js                   # Vue 应用入口
│   ├── App.vue                   # 根组件（导航栏 + 页脚 + RouterView）
│   ├── style.css                 # 全局基础样式
│   ├── theme.css                 # 红色法律主题 CSS 变量
│   ├── constants.js              # API 地址 & 存储键常量
│   ├── router/
│   │   └── index.js              # Vue Router 路由配置
│   ├── views/
│   │   ├── Home.vue              # 首页（Hero + 功能 + 流程 + 案例 + CTA）
│   │   ├── Chat.vue              # 核心庭审对话页（2D/3D 视图）
│   │   ├── login.vue             # 登录 / 注册 / 角色工作台
│   │   ├── history.vue           # 历史评价报告
│   │   ├── AboutUs.vue           # 关于我们
│   │   └── CourtRoomView.vue     # 3D 法庭场景视图
│   ├── components/
│   │   └── CourtRoom3D.vue       # Three.js 3D 法庭组件
│   └── assets/                   # 图片 / 视频 / 字体
│
├── public/                       # 静态资源
│   ├── index.html                # Unity WebGL 宿主页
│   ├── Build/                    # Unity WebGL 构建产物
│   └── TemplateData/             # Unity 模板资源
│
├── main.py                       # ★ 主对话服务 (port 8000)
├── rbac_auth.py                  # ★ RBAC 认证服务 (port 8001)
├── task_management.py            # ★ 任务管理服务 (port 8002)
├── court_evaluation_backend.py   # ★ 庭审评估服务 (port 8003)
├── case_model.py                 # ★ 案件管理服务 (port 8004)
├── config.py                     # 共享配置（读取 .env）
├── start_services.py             # 一键启动脚本
│
├── screenshots/                  # 📸 截图目录（自行放置）
│   ├── home-hero.png
│   ├── features.png
│   ├── process.png
│   ├── cases.png
│   ├── chat-2d.png
│   ├── chat-3d.png
│   ├── evaluation.png
│   └── login.png
│
└── dist/                         # 前端构建输出
```

---

## 🎨 设计系统

项目使用统一的 **CSS 自定义变量（Design Tokens）** 定义红色法律主题。所有颜色变量集中在 `src/theme.css`：

| Token | 色值 | 说明 |
|---|---|---|
| `--color-primary` | `#8B1A1A` | 深红主色 |
| `--color-accent` | `#D7000F` | 强调红 |
| `--color-gold` | `#C9A96E` | 法槌金点缀 |
| `--color-bg-warm` | `#F5F0EB` | 暖白页面背景 |
| `--gradient-hero-light` | 浅红渐变 | Hero 横幅背景 |

---

## 📄 许可证

本项目为山东政法学院网络空间安全学院教学实践项目。

---

<p align="center">
  <b>Made with ❤️ by 山政网安开发团队</b><br/>
  <sub>© 2025 山政网安开发团队版权所有</sub>
</p>
