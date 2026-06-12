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

## 参考资源

- `assets/templates/` — 各组件完整模板代码，生成时直接读取
- `references/design-guide.md` — 详细设计规范和 UI 参考
- 生成过程中如遇不确定的细节，参考 `assets/templates/` 下的完整实现
