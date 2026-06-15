# 微信小程序 AI 聊天界面 — 集成说明

## 快速开始

### 1. 复制文件

将以下目录复制到你的小程序项目的 `miniprogram/` 目录下：

```
components/chat-interface/    → miniprogram/components/chat-interface/
components/markdown-renderer/ → miniprogram/components/markdown-renderer/
utils/chat-api.js             → miniprogram/utils/chat-api.js
pages/chat/                   → miniprogram/pages/chat/
```

### 2. 注册页面和组件

在 `app.json` 中：

```json
{
  "pages": [
    ...现有页面,
    "pages/chat/chat"
  ],
  "usingComponents": {}
}
```

> 如果需要在其他页面使用，也在对应页面的 `.json` 中注册 `chat-interface` 组件。

### 3. 准备图标资源

在 `miniprogram/imgs/` 目录下放置以下 SVG/PNG 图标文件（可使用任意图标库或自行设计）：

| 文件名 | 用途 |
|--------|------|
| `send.svg` | 发送按钮 |
| `stop.svg` | 停止生成按钮 |
| `voice.svg` | 语音输入切换 |
| `keyboard.svg` | 键盘输入切换 |
| `copy.svg` | 复制按钮 |
| `thumb-up.svg` | 点赞按钮 |
| `thumb-down.svg` | 点踩按钮 |
| `clear.svg` | 清空对话 |
| `new-chat.svg` | 新建对话 |
| `set.svg` | 扩展工具栏（加号） |
| `loading.svg` | 加载动画 |
| `error-circle.svg` | 错误提示 |
| `toBottom.svg` | 回到底部箭头 |
| `uploadImg.svg` | 上传图片 |
| `file.svg` | 文件图标 |
| `close-filled.png` | 关闭/移除 |
| `internet.svg` | 联网搜索（关闭态） |
| `internetUse.svg` | 联网搜索（开启态） |

### 4. 配置参数

编辑 `pages/chat/chat.js`，根据需要修改配置：

```js
data: {
  welcomeMsg: '你好！我是 AI 助手，有什么可以帮你的？',
  apiMode: 'mock',    // 'mock' = 本地模拟 | 'real' = OpenAI/DeepSeek | 'dify' = Dify 对话型应用
  // 启用真实 API：
  // apiMode: 'real',
  // apiEndpoint: 'https://your-api.com/v1/chat/completions',
  // 启用 Dify：
  // apiMode: 'dify',
}
```

### 5. 运行

在微信开发者工具中编译预览，即可看到 AI 聊天界面。

---

## 对接真实后端 API

### DeepSeek API

```js
// pages/chat/chat.js
const { setApiKey } = require('../../utils/chat-api');

Page({
  data: {
    apiMode: 'real',
    apiEndpoint: 'https://api.deepseek.com/v1/chat/completions',
  },
  onLoad() {
    // 方式 1：直接设置（开发阶段，不安全）
    setApiKey('sk-your-deepseek-api-key');

    // 方式 2：通过后端代理获取（推荐，安全）
    // wx.request({ url: 'https://your-backend.com/get-token', ... })
  },
});
```

### Dify 对话型应用

```js
// pages/chat/chat.js
const { DifyAPI } = require('../../utils/chat-api');

Page({
  data: {
    apiMode: 'dify',
  },
  onLoad() {
    // 初始化 Dify API
    DifyAPI.init(
      'app-YOUR_DIFY_API_KEY',                         // Dify API Key（从 Dify 后台获取）
      'http://10.43.128.231:61000/ai/v1'               // 基础 URL（含 Nginx /ai/ 前缀）
    );
  },
});
```

#### Dify 所需后端环境

- Nginx 反向代理：将 `/ai/*` 路由到 Dify 服务端口（如 21326），自动剥离 `/ai/` 前缀
- **Nginx `client_max_body_size` 必须 ≥ 50m**（默认 1MB 会导致图片上传 413）
- Dify 服务需暴露端口并通过 `host.docker.internal` 或 IP 可达
- 用户标识通过业务系统的 `GET /db/auth/me` 获取

#### Dify API Key 安全

API Key **不要硬编码在前端**，建议存储在 `config/api.js` 中并加入 `.gitignore`：

```js
// config/api.js（不提交到仓库）
const API = {
  DIFY_API_KEY: 'app-xxxxxxxxxxxxx',
  AI_CHAT: base_url + '/ai/v1/chat-messages',
  AI_FILE_UPLOAD: base_url + '/ai/v1/files/upload',
  // ...
};
```

### 自定义后端

修改 `utils/chat-api.js` 中的 `streamChat` 函数，适配你自己的 SSE 格式。

---

## 自定义样式

所有颜色通过 CSS 变量控制，修改 `components/chat-interface/index.wxss` 中的变量即可：

```css
page {
  --brand: #436af4;          /* 品牌色 */
  --bg-primary: #ffffff;     /* 主背景 */
  --bubble-user: #f3f5fb;    /* 用户气泡 */
  /* ...更多变量见文件顶部 */
}
```

暗黑模式颜色在 `@media (prefers-color-scheme: dark)` 块中修改。

---

## 组件属性一览

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| welcomeMsg | String | "你好！…" | 初始欢迎语 |
| placeholder | String | "输入消息..." | 输入框占位文字 |
| userAvatar | String | "" | 用户头像 URL |
| aiAvatar | String | "" | AI 头像 URL |
| title | String | "AI 助手" | 顶部标题 |
| suggestions | Array | [...] | 推荐问题列表 |
| showCopyBtn | Boolean | true | 显示复制按钮 |
| showClearBtn | Boolean | true | 显示清空按钮 |
| showFeedbackBtn | Boolean | true | 显示点赞/点踩 |
| enableDarkMode | Boolean | true | 适配暗黑模式 |
| enableVoice | Boolean | false | 启用语音输入 |
| enableFileUpload | Boolean | false | 启用文件上传 |
| enableWebSearch | Boolean | false | 启用联网搜索开关 |
| apiMode | String | "mock" | API 模式 |
| apiEndpoint | String | "" | API 地址 |

## 事件

| 事件名 | 参数 | 说明 |
|--------|------|------|
| messageschange | `{messages}` | 消息列表变更 |
| send | `{content}` | 用户发送消息 |
