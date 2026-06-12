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
