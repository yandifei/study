# 微信小程序底部输入区域 — 踩坑总结与可复用模板

> 页面：`pages/search` | 场景：AI 聊天输入框 + 图片预览 + 发送按钮

---

## 一、踩过的坑

| # | 问题 | 现象 | 根因 | 最终方案 |
|---|------|------|------|----------|
| 1 | 底部间距不足 | 输入框紧贴 TabBar，视觉拥挤、易误触 | 用空 div 占位（`safe-bottom`），高度不可控 | `.footer-area` 直接设 `padding-bottom` |
| 2 | 上传按钮与输入框不对齐 | 图标偏高/偏低 | `.input-row` 用 `align-items: flex-end` | 改为 `align-items: center` |
| 3 | 输入框不随行数增长 | 多行文字被截断 | 去掉 `auto-height` 后高度固定死 | `auto-height="{{true}}"` + CSS `max-height` 封顶 |
| 4 | 添加图片后底部被挤出屏幕 | footer 长高但 message-scroll 不收缩 | flex 子元素默认 `min-height: auto`，拒绝缩小 | `message-scroll` 设 `flex: 1 1 0` + `min-height: 0` |
| 5 | `overflow: hidden` 裁剪 footer | 页面底部内容被切掉 | 根容器 `overflow: hidden` + `100vh` 固定高度 | 去掉 `overflow: hidden`，靠 flex 自己分配空间 |

---

## 二、核心原理

```
┌─ .chat-main (flex容器, min-height:0) ─────┐
│  .nav-bar        flex-shrink:0  高度固定    │
│  .message-scroll  flex:1 1 0   自适应伸缩   │  ← 唯一可伸缩区域
│  .footer-area    flex-shrink:0  随内容长高   │  ← 图片预览撑高时向上"借"空间
└────────────────────────────────────────────┘
```

**铁律**：三块区域中只有 `.message-scroll` 可伸缩（`flex: 1 1 0` + `min-height: 0`），另外两块固定不缩（`flex-shrink: 0`）。footer 长高时，scroll 自动让位——**底部锚定不动，向上生长**。

---

## 三、可复用模板

### 3.1 WXML 片段

```xml
<!-- ===== 底部输入区域 ===== -->
<view class="footer-area">

  <!-- 图片/文件预览行（按需显示） -->
  <view wx:if="{{uploadedFiles.length > 0}}" class="file-preview-row">
    <view wx:for="{{uploadedFiles}}" wx:key="id" class="file-preview-item">
      <image class="file-preview-img" src="{{item.path}}" mode="aspectFill"
             bindtap="handlePreviewFile" data-path="{{item.path}}" />
      <view class="file-remove-btn" catchtap="handleRemoveFile" data-id="{{item.id}}">
        <text class="file-remove-x">✕</text>
      </view>
    </view>
  </view>

  <!-- 输入框行 -->
  <view class="input-row">
    <!-- 左侧功能按钮（可选） -->
    <image class="input-btn upload-btn" src="/res/add_files.png"
           mode="aspectFit" bindtap="handleChooseImage" />

    <!-- 输入框 -->
    <view class="textarea-wrapper">
      <textarea
        class="message-textarea"
        value="{{inputValue}}"
        placeholder="输入消息..."
        placeholder-style="color: #bbb"
        maxlength="2000"
        auto-height="{{true}}"
        show-confirm-bar="{{false}}"
        confirm-type="send"
        cursor-spacing="12"
        adjust-position="{{true}}"
        bindinput="onInputChange"
        bindfocus="onInputFocus"
        bindconfirm="handleSend"
      />
    </view>

    <!-- 发送/停止按钮（二选一） -->
    <view wx:if="{{inputValue && !isGenerating}}" class="send-btn" bindtap="handleSend">
      <text class="send-icon">↑</text>
    </view>
    <view wx:elif="{{isGenerating}}" class="stop-btn" bindtap="handleStop">
      <text class="stop-icon">■</text>
    </view>
  </view>
</view>
```

### 3.2 WXSS 样式

#### 底部区域本体

```css
.footer-area {
  flex-shrink: 0;                    /* 不压缩 */
  background-color: #FFFFFF;
  border-top: 1rpx solid #E4E8F0;
  padding: 10rpx 15rpx;
  padding-bottom: calc(24rpx + env(safe-area-inset-bottom));
  box-shadow: 0 -4rpx 24rpx rgba(75,112,253,0.06);  /* 悬浮感 */
}
```

#### 图片预览行

```css
.file-preview-row {
  display: flex;
  gap: 14rpx;
  padding: 10rpx 6rpx 16rpx;
  overflow-x: auto;                  /* 横向滚动 */
}
.file-preview-item {
  position: relative;
  width: 95rpx; height: 95rpx;
  border-radius: 14rpx;
  overflow: hidden;
  flex-shrink: 0;
}
.file-preview-img { width: 100%; height: 100%; }
.file-remove-btn {
  position: absolute; top: -4rpx; right: -4rpx;
  width: 40rpx; height: 40rpx;
  border-radius: 50%;
  background-color: rgba(0,0,0,0.55);
  display: flex; align-items: center; justify-content: center;
}
.file-remove-x { font-size: 20rpx; color: #fff; }
```

#### 输入框行

```css
.input-row {
  display: flex;
  align-items: center;               /* 垂直居中，图标与输入框对齐 */
  gap: 12rpx;
}
```

#### 左侧按钮

```css
.input-btn {
  width: 80rpx; height: 80rpx;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
  border-radius: 50%;
  padding: 10rpx;
  box-sizing: border-box;
}
```

#### 输入框外框

```css
.textarea-wrapper {
  flex: 1;
  min-height: 10px;
  display: flex; align-items: center;
  border: 2rpx solid #E4E8F0;
  border-radius: 28rpx;              /* 大胶囊 */
  box-sizing: border-box;
  background-color: #FFFFFF;
  padding: 0 6rpx;
}
```

#### 输入框本体

```css
.message-textarea {
  width: 100%;
  padding: 14rpx 22rpx;
  font-size: 30rpx;
  line-height: 1.5;
  color: #1a1a1a;
  max-height: 208rpx;                /* 4行封顶，auto-height 达上限后自动滚动 */
}
```

#### 发送/停止按钮

```css
.send-btn, .stop-btn {
  width: 64rpx; height: 64rpx;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.send-btn { background-color: #4B70FD; }
.stop-btn { background-color: #e84f50; }
.send-icon { font-size: 32rpx; color: #fff; font-weight: bold; }
.stop-icon { font-size: 24rpx; color: #fff; }
```

### 3.3 父容器必需的 flex 约束 ⭐

```css
/* 根容器 — 不要设 overflow:hidden */
.chat-page {
  height: 100vh;
  display: flex;
  flex-direction: row;
}

/* 聊天区域主容器 */
.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;                     /* ★ 允许收缩 */
}

/* 消息滚动区（唯一可伸缩区域） */
.message-scroll {
  flex: 1 1 0;                       /* ★ 可缩至零 */
  min-height: 0;                     /* ★ 允许低于内容高度 */
}
```

---

## 四、记忆口诀

1. **flex 三兄弟**：导航不缩、消息可缩、输入不缩
2. **`min-height: 0`** 是钥匙——没有它，flex 子元素死活不缩到内容以下
3. **`flex: 1 1 0`** 而非 `flex: 1`——基准为 0 才能真正按比例伸缩
4. **别在根容器加 `overflow: hidden`**——底部长高时会被裁剪
5. **`auto-height` + `max-height`**——1→4 行自然增长，超出自动滚动
