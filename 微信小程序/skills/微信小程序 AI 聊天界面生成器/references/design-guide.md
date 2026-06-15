# 微信小程序 AI 聊天界面设计规范

## 色彩系统

### 亮色模式

| 用途 | 色值 | CSS 变量 |
|------|------|----------|
| 主背景 | `#ffffff` | `--bg-primary` |
| 次级背景 | `#f5f5f7` | `--bg-secondary` |
| 输入区背景 | `#f3f4f6` | `--bg-input` |
| 主文字 | `#333333` | `--text-primary` |
| 辅助文字 | `#8b8b8b` | `--text-secondary` |
| 用户气泡背景 | `#f3f5fb` | `--bubble-user` |
| 品牌色/发送按钮 | `#436af4` | `--brand` |
| 品牌浅色 | `#dbeafe` | `--brand-light` |
| 边框色 | `#f3f3f3` | `--border` |
| 浅阴影 | `rgba(99,99,99,0.1)` | `--shadow` |
| 行内代码背景 | `#f0f0f0` | `--code-bg` |
| 代码块背景 | `#282c34` | `--code-block-bg` |
| 错误/危险色 | `#e84f50` | `--danger` |
| 成功/确认色 | `#1aad19` | `--success` |

### 暗黑模式

| 用途 | 色值 | CSS 变量 |
|------|------|----------|
| 主背景 | `#1a1a2e` | `--bg-primary` |
| 次级背景 | `#16213e` | `--bg-secondary` |
| 输入区背景 | `#1e2a45` | `--bg-input` |
| 主文字 | `#e0e0e0` | `--text-primary` |
| 辅助文字 | `#a0a0a0` | `--text-secondary` |
| 用户气泡背景 | `#1a2744` | `--bubble-user` |
| 品牌色 | `#5b8af7` | `--brand` |
| 代码块背景 | `#1e1e2e` | `--code-block-bg` |

## 字体规范

| 用途 | 字号 | 字重 |
|------|------|------|
| 标题栏 | 18px (36rpx) | 500 |
| 消息正文 | 16px (32rpx) | 400 |
| 辅助文字/时间 | 12px (24rpx) | 300 |
| 代码 | 14px (28rpx) | 400 (monospace) |
| 辅助按钮 | 12px (24rpx) | 300 |

行高：消息正文 1.8，代码 1.5

## 间距系统

| 元素 | 间距值 |
|------|--------|
| 页面水平 padding | 24rpx |
| 消息之间 margin-bottom | 16px (32rpx) |
| 气泡内 padding | 24rpx |
| 输入区内部 gap | 10rpx |
| 工具栏按钮间距 | 20rpx |
| 输入框整体 padding | 0 16rpx 24rpx |

## 圆角规范

| 元素 | 圆角值 |
|------|--------|
| 用户消息气泡 | 12rpx 0 12rpx 12rpx |
| AI 消息气泡 | 0 12rpx 12rpx 12rpx（或统一 12rpx） |
| 输入框 | 16rpx |
| 胶囊按钮（发送） | 50rpx |
| 功能卡片/推荐问题 | 12rpx |
| 代码块 | 12rpx |

## 动效规范

- 过渡时间：0.3s ease（通用）
- 抽屉展开：0.3s ease（滑动 + 渐变）
- 加载动画：旋转 1s linear infinite
- 消息气泡出现：fadeIn 0.3s + translateY(10px→0)
- 闪烁光标：opacity 0→1，0.8s step-end infinite

## 图标尺寸规范

| 场景 | 尺寸 |
|------|------|
| 功能图标（语音、加号等） | 58rpx × 58rpx |
| 消息操作图标（复制、点赞等） | 36rpx × 36rpx |
| 文件类型图标 | 60rpx × 60rpx |
| 导航栏图标 | 48rpx × 48rpx |
| 头像 | 56rpx × 56rpx（圆形，border-radius: 28rpx） |
| 加载指示器 | 28rpx × 28rpx |

## 消息气泡规范

### 用户消息
- 靠右显示（`justify-content: flex-end`）
- 背景色：`var(--bubble-user)`（浅蓝）
- 圆角：左上大圆角，其他正常 `border-radius: 12rpx 0 12rpx 12rpx`
- 最大宽度：80%
- 外边距：`margin-left: 32rpx; margin-right: 32rpx`

### AI 消息
- 靠左显示
- 背景色：透明或白色
- 可选左侧头像（56rpx 圆形）
- 最大宽度：85%
- 内容区底部显示操作按钮行（复制、点赞、点踩、语音播放）

## 输入区域规范

- 固定在页面底部，不随内容滚动
- 包含三层：
  1. 功能开关行（如联网搜索按钮，绝对定位在输入框上方）
  2. 文件预览行（横向滚动，每项 110px 宽）
  3. 输入框行（flex 布局，align-items: flex-end）
- 输入框最小高度 54px（一行），最大高度 160px（约 5 行）
- 发送按钮：有内容时显示蓝色圆形按钮（58rpx），无内容时隐藏
- 发送中：发送按钮替换为停止按钮（红色圆形）

## 图片附件展示规范

### 已选待发送图片（输入区上方）

- 横向滚动行，位于输入框上方
- 图片缩略图 95rpx × 95rpx，圆角 14rpx
- 右上角圆形删除按钮（40rpx，半透明黑底 + 白色 ×）
- 间距 14rpx
- 最多 3 张（Dify 默认限制）

### 用户消息中的图片附件

- 显示在消息文本上方（消息气泡内）
- 图片缩略图 160rpx × 160rpx，圆角 12rpx
- 点击调用 `wx.previewImage` 进入大图模式
- 使用 `f.path || f.url` 同时支持本地路径和远程 URL
- 图片容器使用 flex-wrap 布局，gap 10rpx

### 关键字段对齐

```
JS fileRefs: { id, path, url, type, upload_file_id }
WXML:       f.path || f.url  (wx:key="id")
```
**常见 bug**：JS 中存 `_path`，WXML 中取 `f.path` → 字段名不一致导致图片不显示。

## 思考过程（<think>）折叠规范

### 折叠按钮（think-toggle）

- 浅蓝底 (`var(--brand-soft)`) 胶囊型，padding 12rpx 16rpx
- 圆角 10rpx，位于 AI 消息正文上方
- 文案：`▸ 💭 思考过程`（折叠态）/ `▾ 💭 思考过程`（展开态）
- 字号 24rpx，颜色 `var(--brand)`
- 点击切换 `showThought` 状态

### 思考内容区（think-content）

- 灰色代码风格背景 (`var(--code-bg)`)
- padding 16rpx 20rpx，圆角 10rpx
- 左侧品牌色竖线 (`border-left: 4rpx solid var(--brand)`)
- 字号 24rpx，辅助文字色 (`var(--text-secondary)`)
- 行高 1.6，white-space: pre-wrap
- **max-height: 400rpx，overflow-y: auto**（移动端关键约束）
- 默认不渲染（`wx:if="{{item.thought && item.showThought}}"`）

### 状态管理

- 消息对象需初始化 `thought: ''` 和 `showThought: false`
- SSE 流接收到 `<think>` 块时实时剥离，存入 `thought` 字段
- `showThought` 默认 `false`（折叠），用户手动点击展开

---

## DeepSeek 纯白极简风格（v2 配色方案）

纯白背景 + 无头像 + 悬浮胶囊输入框，完全复刻 DeepSeek App 的清爽视觉。

### 亮色模式

| 用途 | 色值 | CSS 变量 |
|------|------|----------|
| 主背景 | `#FFFFFF` | `--bg-primary` |
| 次级背景 | `#F7F7F8` | `--bg-secondary` |
| 输入区背景 | `#F5F5F6` | `--bg-input` |
| 主文字 | `#1a1a1a` | `--text-primary` |
| 辅助文字 | `#8F959E` | `--text-secondary` |
| 用户气泡 | `#F3F0FF`（淡蓝紫） | `--bubble-user` |
| 品牌色 | `#4B70FD` | `--brand` |
| 品牌浅色 | `#EEF2FF` | `--brand-light` |
| 边框色 | `#EEEEEE` | `--border` |
| 微阴影 | `rgba(0,0,0,0.04)` | `--shadow` |
| 思考过程背景 | `#F8F8F9` | `--think-bg` |

### v1 → v2 关键差异

| 元素 | v1 初版 | v2 纯白版 |
|------|---------|-----------|
| 页面背景 | `#EAF1FF` 浅蓝 | `#FFFFFF` 纯白 |
| 导航栏 | `#4B70FD` 蓝底白字 | `#FFFFFF` 白底黑字 |
| 用户气泡 | 白色 `#FFFFFF` | `#F3F0FF` 淡蓝紫 |
| AI 气泡 | 白底 + 蓝左边框 + 阴影 | 纯白无边框无阴影 |
| 用户/AI 头像 | 显示 | **完全隐藏** |
| 输入框 | 灰底贴边 | 白底悬浮胶囊 + 明显底部间距 |
| 思考过程 | 无 | 灰色折叠块 |
| 操作按钮 | 复制 · 点赞 · 点踩 | 复制 · 点赞 · 点踩 · **重新生成** |

### 无头像设计

v2 隐藏所有消息头像，对话区域更干净：

```html
<!-- 用户消息 — 无头像 -->
<view class="message-row user-row">
  <view class="message-bubble user-bubble">...</view>
</view>

<!-- AI 消息 — 无头像 -->
<view class="message-row ai-row">
  <view class="message-body">...</view>
</view>
```

### 悬浮胶囊输入框

输入框脱离导航栏和底部，用间距和微妙阴影制造悬浮感：

```css
.footer-area {
  background-color: var(--bg-primary);
  padding: 16rpx 20rpx;
  padding-bottom: calc(32rpx + env(safe-area-inset-bottom));
  /* 不加 border-top，不加 box-shadow——让它"飘"在白色背景上 */
}
```

---

## 底部输入区 flex 布局铁律

### 问题

添加图片预览后 `footer-area` 长高，若不设 `min-height: 0`，`message-scroll` 拒绝收缩导致底部被挤出屏幕。

### 规则

```
┌─ .chat-main (flex容器, min-height:0) ─┐
│  .nav-bar        flex-shrink:0  固定    │
│  .message-scroll  flex:1 1 0  自适应    │  ← 唯一可伸缩区域
│  .footer-area    flex-shrink:0  固定    │  ← 长高时向上"借"空间，底部不动
└────────────────────────────────────────┘
```

```css
.chat-main { flex: 1; display: flex; flex-direction: column; min-height: 0; }
.nav-bar, .footer-area { flex-shrink: 0; }
.message-scroll { flex: 1 1 0; min-height: 0; }  /* ← 可缩至零 */
```

### 底部间距

空 div 占位不可靠，直接用 `padding-bottom`：

```css
.footer-area { padding-bottom: calc(40rpx + env(safe-area-inset-bottom)); }
```

---

## 自定义导航栏对齐公式

`"navigationStyle": "custom"` 后需要手动对齐标题与微信胶囊按钮：

```js
initNavBar() {
  const info = wx.getSystemInfoSync();
  const menu = wx.getMenuButtonBoundingClientRect();
  const gap = menu.top - info.statusBarHeight;
  // gap = 胶囊顶部到状态栏底部的距离
  this.setData({
    statusBarHeight: info.statusBarHeight,
    navBarHeight: gap * 2 + menu.height,  // 内容区：上下等距 + 胶囊高
    totalNavHeight: info.statusBarHeight + gap * 2 + menu.height,
  });
}
```

WXML 双层 + flexbox 居中：

```html
<view class="nav-bar" style="height: {{totalNavHeight}}px; padding-top: {{statusBarHeight}}px;">
  <view class="nav-bar-content" style="height: {{navBarHeight}}px; display:flex; align-items:center;">
    <text class="nav-title">标题</text>
  </view>
</view>
```

---

## 输入框多行增长策略

`auto-height="{{true}}"` + CSS `max-height`，1→4 行自然增长，超出内部滚动。

```html
<textarea auto-height="{{true}}" ... />
```

```css
.message-textarea {
  font-size: 30rpx;
  line-height: 1.5;
  max-height: 208rpx; /* 30×1.5×4 + padding ≈ 208rpx */
}
```

**不要**用 `onLineChange` 手动计算高度设 inline style——计算结果常与实际渲染不一致，且会与 CSS 冲突。

---

## 重新生成按钮

操作行追加 🔄，点击后找上一条用户消息重新发送：

```html
<text class="action-btn" bindtap="handleRegenerate" data-id="{{item.id}}">🔄</text>
```

```js
handleRegenerate(e) {
  const msgs = [...this.data.messages];
  const idx = msgs.findIndex(m => m.id === e.currentTarget.dataset.id);
  const uMsg = msgs.slice(0, idx).reverse().find(m => m.role === 'user');
  if (!uMsg) return;
  msgs.splice(idx, 1);
  this.setData({ messages: msgs });
  this._sendMessage(uMsg.content, uMsg.files || []);
}
```
