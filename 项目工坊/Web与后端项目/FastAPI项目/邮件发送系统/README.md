# Nebula Mail — 邮件批量调度中心

基于 FastAPI + SQLite 的企业级邮件批量调度系统，支持 **11 种邮件模板**、**定时发送**、**批量管理**、**Pydantic 邮箱校验**、**Web 可视化管理**。

---

## 快速开始

### 环境要求

- Python ≥ 3.14
- [uv](https://docs.astral.sh/uv/) 包管理器

### 1. 克隆 & 安装

```bash
git clone <repo-url>
cd 邮件发送系统
uv sync
```

### 2. 配置 SMTP 凭据

编辑 `config/.env`：

```env
APP_NAME=你的应用名称
SMTP=你的QQ邮箱授权码
SENDER_EMAIL=你的QQ邮箱@qq.com
```

> QQ 邮箱授权码获取：QQ 邮箱 → 设置 → 账户 → POP3/SMTP 服务 → 开启 → 生成授权码

### 3. 启动

```bash
uv run main.py
```

浏览器打开 **`http://localhost:41124`**（端口由 `config/settings.toml` 配置）。

---

## 技术栈

| 类别 | 技术 | 说明 |
|------|------|------|
| Web 框架 | FastAPI 0.136+ | 异步高性能，自动 OpenAPI 文档 |
| ASGI | Uvicorn 0.49+ | 轻量高性能服务器 |
| 数据库 | SQLite3 (WAL) | 零配置，单文件存储 |
| 数据校验 | Pydantic 2.13+ / EmailStr | 严格邮箱校验 |
| 邮件协议 | SMTP SSL (QQ 邮箱) | smtp.qq.com:465 |
| 前端 | HTML5 + CSS3 + Vanilla JS | 零框架，黑白双主题 |
| 日志 | logging + colorlog | 彩色控制台输出 |
| 包管理 | uv | 快速依赖解析 |

---

## 功能概览

### 📧 11 种邮件模板

| 模板 | 场景 | 关键变量 |
|------|------|----------|
| `VERIFY_CODE` | 邮箱验证码 | `verification_code` |
| `PASSWORD_RESET` | 密码重置 | `user_name`, `reset_link`, `ip`, `os_browser` |
| `PASSWORD_CHANGED` | 密码修改通知 | `user_name`, `change_time`, `ip`, `device` |
| `LOGIN_ALERT` | 异地登录提醒 | `user_name`, `login_time`, `location`, `ip`, `device` |
| `EMAIL_CHANGE` | 邮箱变更确认 | `user_name`, `old_email`, `new_email`, `cancel_link` |
| `ORDER_CONFIRM` | 订单确认 | `user_name`, `order_id`, `items[]`, `total`, `pay_method` |
| `SHIP_NOTIFY` | 物流发货 | `user_name`, `order_id`, `tracking_no`, `carrier`, `address` |
| `REFUND_STATUS` | 退款进度 | `user_name`, `order_id`, `refund_amount`, `status`, `reason` |
| `ACCOUNT_WELCOME` | 注册欢迎 | `user_name`, `onboarding_steps[]`, `verify_link` |
| `PROMO_BATCH` | 促销优惠券 | `user_name`, `event_title`, `coupon_code`, `goods[]` |
| `NEWSLETTER` | 周刊资讯 | `user_name`, `subject`, `articles[]` |

### ⚡ 批量创建与定时调度

- 一次创建 N 个收件人的同模板任务
- 支持即时发送（默认）和定时发送（未来任意时间）
- 后台线程每 60 秒扫描到期任务，自动发送
- 启动时立即处理遗留到期任务

### 🔍 Pydantic 邮箱校验

- 后端使用 `EmailStr._validate()` 严格校验（RFC 5322）
- 前端点击「校验」逐条验证，精确定位错误行号
- 支持 `.txt` 文件批量导入（一行一邮箱）

### 🎨 Web 管理界面

- **黑白双主题**：一键切换，偏好持久化到 localStorage
- **动态表单**：选择模板后自动生成对应的变量输入字段
- **快速操作栏**：一键发送全部 / 重试全部失败 / 批量删除 / 清空已完成
- **任务详情展开**：点击行查看完整模板变量 JSON 和错误信息
- **错误弹窗**：点击失败徽章查看 SMTP 错误详情
- **状态筛选**：统计卡片 + 标签联动过滤
- **确认对话框**：危险操作二次确认
- **快捷键**：`Ctrl+Enter` 提交表单

---

## 项目结构

```
邮件发送系统/
├── main.py                        # FastAPI 入口（路由 + 生命周期）
├── pyproject.toml                 # 依赖配置
├── README.md                      # ← 本文档
├── config/
│   ├── settings.toml              # 服务器配置 (host/port)
│   ├── logging_config.yaml        # 日志配置
│   ├── .env                       # SMTP 凭据（不入 git）
│   ├── logo.png                   # 邮件内嵌 Logo
│   └── logo.ico                   # 站点图标
├── utils/
│   ├── message_util.py            # 11 个邮件发送函数
│   ├── email_task_db.py           # SQLite CRUD + 11 套模板定义
│   ├── email_dispatcher.py        # 模板分发 + 后台调度线程
│   ├── config_manager.py          # 配置单例管理器
│   ├── path_utils.py              # 路径工具
│   └── qrcode_manager.py          # 二维码工具
├── data_models/                   # Pydantic 数据模型
├── logger/                        # 日志系统（colorlog）
├── templates/
│   ├── verify_code.html           # 11 个邮件 HTML 模板
│   ├── ... (共 11 个)
│   └── web_ui/index/index.html    # Web 管理界面
├── user_data/
│   └── email_tasks.db             # SQLite 数据库文件
├── outputs/                       # 静态文件挂载
└── 文档/                          # 项目文档
    ├── 需求规格说明书.md
    ├── 技术设计文档.md
    ├── 数据库设计文档.md
    ├── 功能说明文档.md
    ├── 项目报告书.md
    └── 渲染模板类型.md
```

---

## API 端点一览

| # | 方法 | 路径 | 说明 |
|---|------|------|------|
| 1 | `GET` | `/` | Web 管理界面 |
| 2 | `GET` | `/api/email-tasks/templates` | 11 种模板定义（含字段信息） |
| 3 | `GET` | `/api/email-tasks?status=` | 任务列表（可选过滤） |
| 4 | `POST` | `/api/email-tasks` | 批量创建任务 |
| 5 | `DELETE` | `/api/email-tasks/{id}` | 删除单个任务 |
| 6 | `POST` | `/api/email-tasks/{id}/send` | 立即发送指定任务 |
| 7 | `POST` | `/api/email-tasks/{id}/retry` | 重试失败任务 |
| 8 | `POST` | `/api/email-tasks/send-due` | 发送所有到期任务 |
| 9 | `POST` | `/api/email-tasks/send-all-pending` | 一键发送全部待发 |
| 10 | `POST` | `/api/email-tasks/resend-failed` | 重试全部失败 |
| 11 | `DELETE` | `/api/email-tasks/batch` | 批量删除（传入 ID 列表） |
| 12 | `DELETE` | `/api/email-tasks/clean/completed` | 清空已发送记录 |
| 13 | `GET` | `/api/email-tasks/stats` | 统计（total/pending/sent/failed） |
| 14 | `POST` | `/api/email-tasks/validate-emails` | Pydantic 批量邮箱校验 |

**统一响应格式**：`{"code": 200, "msg": "...", "data": {...}}`

---

## 文档索引

| 文档 | 内容 |
|------|------|
| [需求规格说明书](文档/需求规格说明书.md) | 功能需求、用例、数据字典、验收标准 |
| [技术设计文档](文档/技术设计文档.md) | 架构、模块设计、API 规格、安全设计 |
| [数据库设计文档](文档/数据库设计文档.md) | 选型分析、ER 图、范式分析、字段详解、并发设计 |
| [功能说明文档](文档/功能说明文档.md) | 15+ 功能详细说明与使用指南 |
| [项目报告书](文档/项目报告书.md) | 瀑布模型回顾、测试报告、经验总结 |
| [渲染模板类型](文档/渲染模板类型.md) | 11 种模板变量参考表 |

---

## 许可证

MIT
