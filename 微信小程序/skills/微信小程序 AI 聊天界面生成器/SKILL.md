---
name: 微信小程序AI聊天界面
description: >
  在微信小程序中快速生成一个类手机端 DeepSeek 软件风格的 AI 用户交互界面。
  该 skill 用于微信小程序原生框架（WXML + WXSS + JS/TS），不依赖第三方 UI 库。
  当用户需要构建微信小程序 AI 聊天界面、智能客服对话页面、ChatBot 对话组件、
  AI 助手交互界面时，应使用本 skill。关键词触发包括："微信小程序聊天"、
  "AI聊天界面"、"DeepSeek风格"、"小程序AI对话"、"智能客服界面"、
  "ChatBot小程序"、"AI助手页面"、"流式对话UI"、"聊天机器人界面"。
tags:
  - 微信小程序
  - AI聊天
  - DeepSeek风格
  - ChatBot
  - 流式对话
  - 聊天界面
  - 小程序组件
compatibility:
  wechat-miniprogram: ">=2.2.3"
  base-library: ">=3.7.7"
---

# 微信小程序 AI 聊天界面生成器

生成一个类手机端 DeepSeek 风格的 AI 聊天界面，适用于微信小程序原生框架。
输出完整的 WXML/WXSS/JS/JSON 文件，开发者直接复制到项目中即可使用。

## 设计语言：DeepSeek 风格

DeepSeek 软件的风格特征，所有生成的 UI 必须遵循以下设计语言：

- **极简配色**：以白色/浅灰为主背景（`#ffffff` / `#f5f5f7`），主色调为深邃蓝（`#436af4` / `#4d6bfe`），文字色使用 `#333`（主文字）/ `#8b8b8b`（辅助文字）。不使用渐变色或花哨的装饰色。
- **圆角语言**：输入框圆角 16rpx，消息气泡圆角 12rpx，按钮圆角 50rpx（胶囊型），功能卡片圆角 8rpx。
- **清爽间距**：消息间距 12px，内边距 24rpx，整体留白充足，避免拥挤感。
- **微妙阴影**：只在必要时使用 `box-shadow`（如浮动按钮 `0 2px 8px rgba(99,99,99,0.2)`），避免过重阴影。
- **图标驱动**：优先使用 SVG 图标代替文字按钮，简洁直观。图标尺寸统一 36-48rpx。
- **流畅动效**：过渡动画 0.3s ease，加载状态使用旋转动画。消息出现使用轻微的 fadeIn + slideUp。

## 架构概览

生成的组件树如下，严格按此结构组织文件：

```
pages/chat/                    ← 聊天页面（使用 chat-interface 组件）
├── chat.wxml                  ← 页面模板（仅引入组件）
├── chat.wxss                  ← 页面样式（空或全局变量）
├── chat.js                    ← 页面逻辑（配置参数）
└── chat.json                  ← 注册 chat-interface 组件

components/chat-interface/    ← 核心聊天界面组件
├── index.wxml                 ← 完整聊天界面模板
├── index.wxss                 ← 样式（含暗黑模式 CSS 变量）
├── index.js                   ← 核心逻辑（消息管理、滚动控制、流式输出）
└── index.json                 ← 子组件声明

components/markdown-renderer/  ← Markdown/代码块渲染子组件
├── index.wxml
├── index.wxss
├── index.js
└── index.json

utils/chat-api.js              ← API 封装（流式请求、SSE 解析、本地模拟）
```

## 生成流程

### 第 1 步：确认配置参数

向用户确认以下关键配置。**提供默认值，用户可直接回车跳过。** 除非用户明确要求，否则不要跳过此步骤。

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `welcomeMsg` | `"你好！我是 AI 助手，有什么可以帮你的？"` | 初始欢迎语 |
| `placeholder` | `"输入消息..."` | 输入框占位文字 |
| `userAvatar` | `""` | 用户头像 URL，空则显示默认圆形色块 |
| `aiAvatar` | `""` | AI 头像 URL，空则显示 DeepSeek 风格 logo 色块 |
| `showCopyBtn` | `true` | 是否显示每条 AI 回复的复制按钮 |
| `showClearBtn` | `true` | 是否显示清空对话按钮 |
| `showFeedbackBtn` | `true` | 是否显示点赞/点踩反馈按钮 |
| `enableDarkMode` | `true` | 是否适配暗黑模式（使用 CSS 变量 + media query） |
| `enableVoice` | `false` | 是否启用语音输入（长按录音） |
| `enableFileUpload` | `false` | 是否启用文件/图片上传 |
| `streamMode` | `true` | 是否启用流式输出动效 |
| `apiMode` | `"mock"` | API 对接模式：`"mock"`（本地模拟）或 `"real"`（真实后端） |
| `apiEndpoint` | `""` | 后端 API 地址（apiMode 为 "real" 时必填） |
| `titleBarText` | `"AI 助手"` | 顶部标题栏文字 |

### 第 2 步：读取模板并生成文件

读取 `assets/templates/` 下对应组件的模板文件，根据用户确认的配置参数调整默认值后，
写入用户项目的目标目录。**务必逐文件生成，不要省略任何文件。**

文件生成清单（共 15 个文件）：

1. `components/chat-interface/index.json`
2. `components/chat-interface/index.wxml`
3. `components/chat-interface/index.wxss`
4. `components/chat-interface/index.js`
5. `components/markdown-renderer/index.json`
6. `components/markdown-renderer/index.wxml`
7. `components/markdown-renderer/index.wxss`
8. `components/markdown-renderer/index.js`
9. `utils/chat-api.js`
10. `pages/chat/chat.json`
11. `pages/chat/chat.wxml`
12. `pages/chat/chat.wxss`
13. `pages/chat/chat.js`
14. `app-config-patch.json`（需合并到 app.json 的配置片段）
15. `README.md`（集成使用说明）

### 第 3 步：输出集成说明

生成完文件后，输出以下集成指引：

1. 将 `components/` 和 `utils/` 目录复制到小程序项目的 `miniprogram/` 目录下
2. 将 `pages/chat/` 目录复制到 `miniprogram/pages/` 下
3. 在 `app.json` 的 `pages` 数组中添加 `"pages/chat/chat"`
4. 在 `app.json` 中添加 `"usingComponents"` 中所需的全局组件注册
5. 如果对接真实后端（`apiMode: "real"`），修改 `utils/chat-api.js` 中的 `BASE_URL` 和认证逻辑
6. 编译运行，在微信开发者工具中预览

---

## 各组件核心实现要点

### chat-interface（核心组件）

消息数据结构定义（在 `index.js` 的 `data.messages` 中使用）：
```js
{
  id: "msg_1718000000001",     // 唯一标识（时间戳 + 随机数）
  role: "user" | "assistant",  // 发送者角色
  content: "消息文本内容",       // 支持 Markdown 格式
  status: "sent" | "sending" | "streaming" | "failed",
  timestamp: 1718000000000,    // Date.now()
  errorMsg: ""                 // status 为 failed 时的错误描述
}
```

**渲染规则：**
- 用户消息：靠右对齐，浅蓝背景 `var(--bubble-user)`，圆角 `12rpx 0 12rpx 12rpx`，max-width 80%
- AI 回复：靠左对齐，左侧可选圆形头像（56rpx），使用 `markdown-renderer` 渲染内容
- 时间戳：仅当日消息变化较大时在中间显示时间分割线
- 欢迎消息：AI 角色的首条消息，下方展示推荐问题按钮（3 个）

**滚动行为：**
- 新消息到达 → 自动 `scroll-into-view="scroll-bottom"`
- 用户手动上滑 → 暂停自动滚动，显示"回到底部"浮动按钮
- 用户滚回底部或点击按钮 → 恢复自动滚动
- 输入框获焦 → 自动滚到底部

**消息状态 UI：**
- `sending`（等待首 token）：显示旋转加载图标 + "思考中..." 文字
- `streaming`（流式输出中）：内容逐字追加，更新频率 100ms，末尾显示闪烁光标 `▊`（CSS blink 动画）
- `failed`：消息下方显示红色错误图标 + 错误信息 + "重新发送"按钮

**底部输入区域结构：**
```
[功能开关行：联网搜索开关]  ← 可折叠
[文件预览行：已选文件缩略图]  ← 有条件渲染
[输入框行：语音按钮 | textarea | 扩展按钮 | 发送/停止按钮]
```

### markdown-renderer（Markdown 渲染）

使用简化但完整的 Markdown 解析（不依赖 markdown-it），支持：
- **标题**：H1-H6（H1 双下划线，H2 单下划线）
- **粗体/斜体**：`**bold**`、`*italic*`
- **行内代码**：`` `code` `` → 浅灰背景 `#f0f0f0`，红色文字 `#e36209`
- **代码块**：`` ```lang ... ``` `` → 深色背景 `#282c34`，白色文字，头部语言标签 + 复制按钮
- **有序/无序列表**：缩进 1.2em
- **表格**：`overflow-x: auto` 支持横向滚动，斑马纹
- **引用块**：左侧灰色竖线 `border-left: 5px solid #ccc`
- **链接**：蓝色文字，可点击
- **分割线**：`---` → 细灰线

**生成注意事项：**
- 代码块必须带"复制代码"按钮，点击后 `wx.setClipboardData` 复制内容并 toast "已复制"
- 所有文本 `user-select: true`，允许用户选择复制
- 图片宽度限制 480rpx，防止溢出

### chat-api.js（API 封装）

提供两种模式：

**模式 A — 本地模拟（`MockAPI` 类）：**
```js
class MockAPI {
  async sendMessage(messages, onToken, onDone, onError) {
    // 模拟延迟 500ms 后逐 token 输出
    // onToken(token) — 每个 token 回调
    // onDone(fullText) — 完成回调
    // onError(err) — 错误回调
  }
}
```
预置 5 条模拟回复，随机选择，逐字输出模拟流式效果。

**模式 B — SSE 流式对接：**
```js
export function streamChat({ messages, onToken, onDone, onError }) {
  // 使用 wx.request 的 enableChunked 模式
  // 解析 SSE 格式：data: {"choices":[{"delta":{"content":"..."}}]}
  // 处理 [DONE] 结束标记
  // 处理 error 事件
}
```

### 暗黑模式适配

CSS 变量定义在 `chat-interface/index.wxss` 顶部：
```css
page {
  --bg-primary: #ffffff;
  --bg-secondary: #f5f5f7;
  --bg-input: #f3f4f6;
  --text-primary: #333333;
  --text-secondary: #8b8b8b;
  --bubble-user: #f3f5fb;
  --bubble-user-text: #333333;
  --brand: #436af4;
  --brand-light: #dbeafe;
  --border: #f3f3f3;
  --shadow: rgba(99, 99, 99, 0.1);
  --code-bg: #f0f0f0;
  --code-block-bg: #282c34;
  --danger: #e84f50;
}

@media (prefers-color-scheme: dark) {
  page {
    --bg-primary: #1a1a2e;
    --bg-secondary: #16213e;
    --bg-input: #1e2a45;
    --text-primary: #e0e0e0;
    --text-secondary: #a0a0a0;
    --bubble-user: #1a2744;
    --bubble-user-text: #d0d8f0;
    --brand: #5b8af7;
    --brand-light: #1e3050;
    --border: #2a2a4a;
    --shadow: rgba(0, 0, 0, 0.3);
    --code-bg: #2a2a3a;
    --code-block-bg: #1e1e2e;
    --danger: #f06060;
  }
}
```

**关键规则：所有硬编码颜色使用 `var(--xxx)` 替代，绝对不要直接写颜色值。**

### 响应式布局

- 所有尺寸使用 `rpx` 单位（750rpx = 屏幕宽度）
- 消息气泡使用百分比 max-width
- 输入区域固定在底部，使用 flex 布局
- 底部安全区域：`padding-bottom: calc(24rpx + env(safe-area-inset-bottom))`

---

## Dify API 集成模式（生产力级）

Dify 对话型应用使用与 OpenAI/DeepSeek 不同的 API 协议。以下为微信小程序对接 Dify 的完整方案。

### Nginx 路由架构

```
微信小程序 → Nginx(:61000) → /ai/*  → Dify 服务(:21326)
                            → /db/*  → 数据库服务(:21325)
```

Nginx 剥离 `/ai/` 前缀后转发，如 `/ai/v1/chat-messages` → Dify 收到 `/v1/chat-messages`。

### API 端点映射

| 配置 Key | 路径 | 方法 | 说明 |
|----------|------|------|------|
| `AI_CHAT` | `/ai/v1/chat-messages` | POST | 发送对话（SSE 流式） |
| `AI_FILE_UPLOAD` | `/ai/v1/files/upload` | POST | 上传图片（multipart/form-data） |
| `AI_CONVERSATIONS` | `/ai/v1/conversations` | GET/DELETE | 会话列表/删除 |
| `AI_MESSAGES` | `/ai/v1/messages` | GET | 历史消息 |
| `AI_FEEDBACK` | `/ai/v1/messages/{id}/feedbacks` | POST | 点赞/点踩反馈 |
| `AI_PARAMETERS` | `/ai/v1/parameters` | GET | 应用参数/开场白 |

### Dify SSE 事件类型

```
event: message        — LLM 文本块（answer, message_id, conversation_id, task_id）
event: agent_message  — Agent 模式文本块（字段同上）
event: agent_thought  — Agent 思考步骤（thought, observation, tool, tool_input）
event: message_file   — 文件生成事件（id, type, url）
event: message_end    — 流结束标记
event: error          — 错误事件
event: ping           — 心跳（每 10s）
```

### Dify 鉴权

```js
header: { 'Authorization': `Bearer ${API.DIFY_API_KEY}` }
```

API Key 来自 Dify 后台「访问 API」页面，不要硬编码在前端。建议通过 `config/api.js` 中定义 `DIFY_API_KEY`，列入 `.gitignore`。

### 用户标识

Dify 的 `user` 参数用于区分终端用户。获取方式：
```js
// 从自己的数据库服务获取用户 id
request({ url: API.USER_INFO, method: 'GET' }).then(res => {
    const userId = res.data.id || res.data.email || 'anonymous';
});
```
将 `userId` 作为 `user` 字段传给所有 Dify API。

---

## 图片上传与气泡展示（关键踩坑）

### 上传流程

```
用户选择图片 → wx.chooseMedia() → 本地预览
→ 点击发送 → wx.uploadFile() 上传到 Dify
→ 拿到 upload_file_id → 随 chat-messages 请求发送
```

### wx.uploadFile 的响应解析陷阱

**宿命级 bug**：新版微信 SDK（如 lib 3.16.0+）可能已自动将 JSON 响应解析为对象，`res.data` 不再是字符串。必须同时处理两种类型：

```js
let data;
if (typeof res.data === 'string') {
    try { data = JSON.parse(res.data); } catch (e) { /* 非 JSON 响应 */ }
} else if (typeof res.data === 'object' && res.data !== null) {
    data = res.data;  // SDK 已自动解析
}
```

### 图片在气泡中显示的字段对齐

用户消息气泡中显示图片缩略图，**必须确保 JS 字段名与 WXML 引用一致**：

```js
// JS — _uploadFilesThenSend 返回的 fileRefs
fileRefs.push({
    id: result.value.id,        // WXML wx:key="id" 使用
    path: files[index].path,    // ← 注意是 path，不是 _path
    url: '',                    // 远程 URL（如有）
    type: 'image',
    transfer_method: 'local_file',
    upload_file_id: result.value.id,
});
```

```html
<!-- WXML — 用户消息气泡内 -->
<view wx:if="{{item.files && item.files.length > 0}}" class="msg-images">
    <image wx:for="{{item.files}}" wx:key="id" wx:for-item="f"
        class="msg-image-item" src="{{f.path || f.url}}" mode="aspectFill"
        bindtap="handlePreviewFile" data-path="{{f.path || f.url}}" />
</view>
```

### Nginx 413 Request Entity Too Large

**默认 `client_max_body_size` 仅 1MB**，图片上传必然触发 413。必须修改 nginx.conf：
```nginx
client_max_body_size 500m;
```

### userId 竞态条件

`loadUserInfo()` 是异步请求。用户可能在 userId 加载完成前点击发送，导致 `user` 参数为空。**必须在 handleSend 中加守卫**：

```js
if (!this.data.userId) {
    wx.showToast({ title: '正在加载用户信息，请稍后再试', icon: 'none' });
    return;
}
```

---

## <think> 思考过程流式剥离（移动端关键优化）

DeepSeek-R1 等推理模型在 `answer` 文本中输出 `<think>...</think>` 标签包裹的思考过程。在移动端小屏幕上，默认展开会占据大半屏且内容对普通用户无意义。

### 流式剥离状态机

必须**在 SSE token 到达时实时剥离**，不能在流结束后再处理（否则思考内容会在流式输出时占屏）：

```js
var THINK_OPEN = '<think>';
var THINK_CLOSE = '</' + 'think>';   // ← 拼接法防止文件写入时被转义
var inThink = false;
var tagBuf = '';      // 跨 chunk 残留缓冲
var thoughtAcc = '';  // 思考内容累加器

onToken: (token) => {
    const combined = tagBuf + token;
    tagBuf = '';
    let display = '';
    let i = 0;
    while (i < combined.length) {
        if (!inThink) {
            if (combined.substring(i, i + 7) === THINK_OPEN) {
                inThink = true; i += 7;
            } else { display += combined[i]; i++; }
        } else {
            if (combined.substring(i, i + 8) === THINK_CLOSE) {
                inThink = false; i += 8;
            } else { thoughtAcc += combined[i]; i++; }
        }
    }
    // 防跨 chunk 截断：检测末尾不完整的 <think> 或 </think> 片段
    // 将其从 display/thoughtAcc 中移除，存入 tagBuf 等下一个 token 拼接
    // ...
    // 更新 messages[idx].content 仅含 display（不含思考内容）
    // 更新 messages[idx].thought 含 thoughtAcc，showThought: false（默认折叠）
}
```

### 折叠 UI

```html
<view wx:if="{{item.thought}}" class="think-toggle" bindtap="handleToggleThought" data-id="{{item.id}}">
    <text>{{item.showThought ? '▾' : '▸'}} 💭 思考过程</text>
</view>
<view wx:if="{{item.thought && item.showThought}}" class="think-content">
    <text user-select="{{true}}">{{item.thought}}</text>
</view>
```

CSS：`.think-toggle` 为浅蓝底胶囊按钮，`.think-content` 为灰色代码风格、`max-height: 400rpx` 可滚动。

### Agent 模式额外处理

Dify Agent 模式还会通过 `agent_thought` SSE 事件推送思考步骤。需在 SSE 解析中增加对应 case 并通过 `onThought` 回调传入。

---

## 反馈（点赞/点踩）与真实 message_id 映射

### 问题根因

本地生成的消息使用 `msg_1718345678_abc123` 格式的 ID，但 Dify 反馈 API 需要 SSE 流返回的 UUID 格式 `message_id`（如 `5ad4cb98-f0c7-4085-b384-88c403be6290`）。

### 解决方案

1. SSE `message` 事件中提取 `json.message_id` → 通过 `onMessageId` 回调传入
2. 存入 `messages[idx].difyMessageId`（独立字段，不覆盖本地 id）
3. `handleFeedback` 中优先使用 `difyMessageId`，回退到本地 `id`

```js
onMessageId: (messageId) => {
    this.setData({ [`messages[${aiIndex}].difyMessageId`]: messageId });
},

handleFeedback(e) {
    const idx = this.data.messages.findIndex(m => m.id === id);
    const realId = (idx >= 0 && this.data.messages[idx].difyMessageId) || id;
    DifyAPI.sendFeedback(realId, rating, this.data.userId).then(...)
}
```

历史消息（通过 `GET /messages` 加载）的 `item.id` 就是真实 Dify ID，应在 `loadMessages` 中直接设 `difyMessageId: item.id`。

### 消息数据结构（完整版）

```js
{
    id: "msg_1718000000001",           // 本地 ID
    difyMessageId: "5ad4cb98-f0c7-...", // Dify 真实 message_id（用于反馈 API）
    role: "user" | "assistant",
    content: "消息文本",
    status: "sent" | "sending" | "streaming" | "failed",
    timestamp: 1718000000000,
    errorMsg: "",
    files: [{ id, path, url, type, ... }],  // 附件（图片等）
    feedback: null | "like" | "dislike",     // 用户反馈状态
    thought: "",           // 思考过程（由 <think> 标签或 agent_thought 提取）
    showThought: false,    // 默认折叠思考过程
}
```

---

## 底部输入区 flex 布局铁律（关键）

添加图片预览后 footer 长高时，若消息滚动区不收缩，底部会被挤出屏幕。**根因**：flex 子元素默认 `min-height: auto`，拒绝缩到内容高度以下。

### 正确的三区域布局

```
┌─ .chat-main (flex容器, min-height:0) ─┐
│  .nav-bar        flex-shrink:0  固定    │
│  .message-scroll  flex:1 1 0  自适应    │  ← 唯一可伸缩
│  .footer-area    flex-shrink:0  固定    │  ← 长高时向上"借"空间
└────────────────────────────────────────┘
```

```css
.chat-main { flex: 1; display: flex; flex-direction: column; min-height: 0; }
.message-scroll { flex: 1 1 0; min-height: 0; }  /* ★ 可缩至零 */
.nav-bar, .footer-area { flex-shrink: 0; }       /* 不压缩 */
```

**记忆口诀**：三块中只有消息区可伸缩（`flex: 1 1 0` + `min-height: 0`），另外两块固定。

### 底部间距

不要用空 div 占位（高度不可控），直接用 `padding-bottom`：

```css
.footer-area {
  padding-bottom: calc(32rpx + env(safe-area-inset-bottom));
}
```

---

## 自定义导航栏精确对齐

`"navigationStyle": "custom"` 后隐藏系统导航栏，需手动计算高度使标题与右侧胶囊按钮垂直居中。

```js
initNavBar() {
  const info = wx.getSystemInfoSync();
  const menu = wx.getMenuButtonBoundingClientRect();
  const gap = menu.top - info.statusBarHeight;          // 胶囊上方间距
  this.setData({
    statusBarHeight: info.statusBarHeight,
    navBarHeight: gap * 2 + menu.height,                 // 内容区 = 上下等距 + 胶囊高
    totalNavHeight: info.statusBarHeight + gap * 2 + menu.height,
  });
}
```

WXML 双层结构，内容区 flexbox `align-items: center` 自动垂直居中标题：

```html
<view class="nav-bar" style="height: {{totalNavHeight}}px; padding-top: {{statusBarHeight}}px;">
  <view class="nav-bar-content" style="height: {{navBarHeight}}px;">
    <!-- 标题与胶囊自然对齐 -->
  </view>
</view>
```

---

## DeepSeek 纯白极简风格（v2）

与初版（蓝色导航栏 + 浅蓝背景）不同，v2 完全复刻 DeepSeek App 的纯白风格：

| 元素 | v1 初版 | v2 纯白版 |
|------|---------|-----------|
| 页面背景 | `#EAF1FF` 浅蓝 | `#FFFFFF` 纯白 |
| 导航栏 | `#4B70FD` 品牌蓝 | `#FFFFFF` 白底 + 黑字 |
| 用户气泡 | 白色 | `#F3F0FF` 淡蓝紫 |
| AI 气泡 | 白底 + 蓝左边框 | 纯白无边框 |
| 头像 | 显示 "我"/"AI" | **隐藏** |
| 输入框 | 灰底贴边 | 白底悬浮胶囊 + 明显间距 |
| 思考过程 | 无 | 灰色折叠块 `▸ 已思考（用时Xs）` |
| 操作按钮 | 复制/点赞/点踩 | 复制/点赞/点踩/**重新生成** |

```css
--bg-primary: #FFFFFF;
--bubble-user: #F3F0FF;
--nav-bg: #FFFFFF;
--border: #EEEEEE;
--shadow: rgba(0,0,0,0.04);
```

---

## Textarea 多行增长策略

用 `auto-height="{{true}}"` + CSS `max-height` 实现 1→4 行自然增长、超出内部滚动：

```html
<textarea auto-height="{{true}}" ... />
```
```css
.message-textarea { max-height: 208rpx; }  /* 30rpx字号 × 1.5行高 × 4行 + padding */
```

不要在 `onLineChange` 中手动算高度设 inline style——既不可靠又会与 CSS 冲突。

---

## 重新生成按钮

在 AI 消息操作行追加 🔄 按钮，点击后找到上一条用户消息重新发送：

```js
handleRegenerate(e) {
  const msgs = [...this.data.messages];
  const idx = msgs.findIndex(m => m.id === e.currentTarget.dataset.id);
  const uMsg = msgs.slice(0, idx).reverse().find(m => m.role === 'user');
  msgs.splice(idx, 1);
  this.setData({ messages: msgs });
  this._sendMessage(uMsg.content, uMsg.files || []);
}
```

---

## 参考资源

- `assets/templates/` — 各组件完整模板代码，生成时直接读取
- `references/design-guide.md` — 详细设计规范和 UI 参考
- `B:\study\微信小程序\期末作业\文档\Dify的API接口文档.md` — Dify 完整 API 参考
- `B:\study\微信小程序\期末作业\文档\微信小程序后端系统架构设计文档.md` — Nginx 路由架构
- 生成过程中如遇不确定的细节，参考 `assets/templates/` 下的完整实现
