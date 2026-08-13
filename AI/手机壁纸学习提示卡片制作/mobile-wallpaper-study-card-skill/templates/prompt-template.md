# Prompt 模板

## 第一版生成

```text
请制作一张 {{PHONE_MODEL}} 手机学习提醒壁纸。

目标分辨率：
{{RESOLUTION}}

用途：
{{LOCK_OR_HOME}}

视觉风格：
{{STYLE}}

原始角色图：
{{REFERENCE_IMAGE}}

标题：
{{TITLE}}

副标题：
{{SUBTITLE}}

PRIMARY：
{{PRIMARY_KEYWORDS}}

SECONDARY：
{{SECONDARY_KEYWORDS}}

激励语：
{{MOTIVATION}}

布局要求：
1. 顶部保留手机系统 UI 安全区。
2. 标题位于系统时间/组件下方。
3. PRIMARY 位于左侧。
4. 角色位于中间偏右。
5. SECONDARY 位于右下。
6. 激励语位于左下。
7. 人物脸部不得进入锁屏大时间区域。
8. 底部重要内容不得被相机、手电筒、Dock 或 Home 指示条遮挡。
9. 文字必须清晰。
10. 不要为了填满屏幕而放大内容。
```

## 实机截图修订

```text
Image A 是原始壁纸。
Image B 是用户真实手机截图。

只使用 Image B 判断系统 UI 覆盖区域。
不要把 Image B 中的时间、日期、状态栏、相机、手电筒等系统 UI 画进最终图。

保持 Image A 的：
- 角色
- 风格
- 技术关键词
- 字号
- 卡片大小
- 相对布局

根据用户要求整体移动主体。

例如：
将“学习提醒”以及学习提醒以下全部主体内容整体向上移动一点，使标题靠近 8:40 小组件区域底部。

不要放大。
```
