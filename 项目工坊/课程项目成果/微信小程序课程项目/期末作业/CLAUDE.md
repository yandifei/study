# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

**ACG 智能图廊** — 一个由 AI 驱动的、面向 ACG 爱好者的图片鉴赏与智能对话微信小程序。用户可浏览/收藏 ACG 图片，并通过 Dify 大模型平台与 AI 进行多模态对话（上传图片或输入文字，获取图片分析、风格解读、创作建议）。

## 项目结构

```
ACG AI Gallery/          ← 微信小程序前端（主项目）
   app.js / app.json / app.wxss
   config/api.js         ← 集中管理所有 API 端点 URL
   utils/
     request.js          ← 统一请求封装（自动挂 JWT、401 刷新队列）
     dify-api.js         ← Dify 对话型应用 API 封装（SSE 流式对话）
   pages/
     home/               ← 首页（主题分类导航）
     gallery/            ← 图片鉴赏页（网格浏览 + 详情弹窗）
     search/             ← 探索页（AI 多模态对话 + 智能搜索）
     settings/           ← 个人中心（用户信息、收藏入口、退出）
     browse/             ← 浏览记录
     favorite/           ← 收藏列表
     login/              ← 邮箱验证码登录
     protocol/ / privacy/← 用户协议/隐私政策
   components/
     navigation-bar/     ← 自定义导航栏
     acg-images/         ← 图片网格组件（复用）
     acg-images-mp/      ← 图片网格组件（小程序原生版）
   res/                  ← 图标等静态资源

文档/                    ← 项目文档（需求规格、架构设计、数据库设计、API 文档等）
人机版/ / 非人机版/      ← 实验性/草稿版本的页面代码
```

## 技术栈

| 层 | 技术 |
|---|------|
| 前端 | 微信小程序原生框架（glass-easel 组件框架） |
| 后端-数据库服务 | Python FastAPI + Uvicorn，端口 21325 |
| 后端-AI 服务 | 独立项目（端口 21326），对接 Dify 平台 |
| 数据库 | MongoDB 单实例（pymongo 原生异步，不用 ODM） |
| 缓存 | Redis 单实例（Refresh Token、验证码、冷却期） |
| 反向代理 | Nginx（Docker 容器），宿主机 61000 端口，按 `/db/*` / `/ai/*` 路径分流 |
| 内网穿透 | ngrok，将本地 61000 映射到公网 HTTPS |
| AI 平台 | Dify 对话型应用 API（SSE 流式输出） |
| 邮件 | QQ 邮箱 SMTP（发送验证码） |
| 认证 | 邮箱验证码登录 + JWT 双 Token（Access 15min + Refresh 30day） |

## 常用命令

### 后端启动

```bash
# 数据库服务（在 mongodb_service 项目目录）
python main.py                    # Uvicorn 启动，监听 0.0.0.0:21325

# Nginx 容器（可选，单服务调试可跳过）
docker-compose up -d              # 启动 Nginx，容器 8000 → 宿主机 61000

# ngrok 内网穿透（需要 ngrok 客户端）
ngrok http 61000                  # 或直接指向 21325 端口直连调试
```

### 前端开发

```bash
# 用微信开发者工具打开 ACG AI Gallery/ 目录
# 开发环境 Base URL: http://127.0.0.1:61000
# 开发时可在工具中勾选"不校验合法域名"绕过 HTTPS 限制
```

### 环境变量（后端 .env）

- `MONGODB_URL` — MongoDB 连接字符串
- `REDIS_HOST` / `REDIS_PORT` / `REDIS_PASSWORD` — Redis 配置
- `SMTP_HOST` / `SMTP_PORT` / `SMTP_USER` / `SMTP_PASSWORD` — QQ 邮箱 SMTP
- `ACCESS_TOKEN_SECRET_KEY` / `REFRESH_TOKEN_SECRET_KEY` — JWT 签名密钥（两者不同）
- `ALGORITHM` — JWT 算法（HS256）

## 架构要点

### 请求链路

```
微信小程序 → HTTPS → ngrok → Nginx(:61000) → /db/* → 数据库服务(:21325) → MongoDB/Redis
                                             → /ai/* → AI 服务(:21326) → Dify API
```

### 前端核心机制

1. **环境自动切换**（[config/api.js](ACG AI Gallery/config/api.js)）：通过 `wx.getAccountInfoSync().miniProgram.envVersion` 自动区分 develop / trial / release，对应不同 BASE_URL。所有 API 端点集中定义在此文件。

2. **请求拦截器**（[utils/request.js](ACG AI Gallery/utils/request.js)）：封装 `wx.request`，自动附带 `Authorization: Bearer <access_token>` 和 `ngrok-skip-browser-warning` 头。遇到 401 时进入刷新队列（并发锁），只发一次 refresh 请求，其他 401 排队等待，成功后批量重试。Pass `skipAuth: true` 跳过认证（登录/发送验证码）。

3. **Dify SSE 流式对话**（[utils/dify-api.js](ACG AI Gallery/utils/dify-api.js)）：使用 `wx.request` + `enableChunked: true` + `onChunkReceived` 解析 SSE 事件流。支持 `message`/`agent_thought`/`message_end`/`error` 事件，`<think>` 标签内容自动折叠展示。注意：`onChunkReceived` 在微信开发者工具模拟器中不可用，需真机测试流式效果。

### 关键设计决策

- **MongoDB 嵌入式文档**：浏览和收藏记录嵌入 `users` 文档，不用独立集合。浏览上限 1000 条（`$slice: -1000`），收藏无上限（`$pull` + `$push` 去重）。子文档冗余 `image_url` 避免 JOIN。
- **Redis RESP2 强制**：`redis-py` 6.x 默认 RESP3 会在认证前发 `HELLO` 导致 `AuthenticationError`，后端显式设置 `protocol=2`。
- **邮箱验证码登录**：不使用微信授权登录。验证码 5min 有效（一次性消费），60s 冷却。新用户验证码即注册。
- **Token Rotation**：Refresh Token 每次使用时旧 token 立即作废换新，检测到重放时撤销该用户全部会话。Access Token 的 `exp` 和 Refresh Token 的 `jti` 双重校验。
- **不使用 ODM**：pymongo 原生异步 + pydantic BaseModel 做数据校验，不用 Beanie（motor 已弃用）。

### 数据库索引

- `users`: `email` unique, `username`
- `images`: `url` unique, `type`, `created_at` descending

## 已知待实现

- `GET /topics` 和 `GET /images?topic=&limit=&skip=` 接口（后端 + 前端）
- 首页主题导航、设置页个人档案的前端 UI 完善
- Dify API Key 生产环境应移至后端代理（当前在 `config/api.js` 中）

## 常见问题

- **代码质量面板误报 navigation-bar**：微信开发者工具的静态分析 Bug，navigation-bar 组件引用正确，忽略该提示或关闭代码质量面板。
- **收藏接口上线后不可访问**：检查 ngrok 隧道是否正常、Nginx 路由 `/db/*` 是否正确转发。
- **Redis 认证报错**：确认后端 `redis.Redis(protocol=2)` 强制 RESP2。