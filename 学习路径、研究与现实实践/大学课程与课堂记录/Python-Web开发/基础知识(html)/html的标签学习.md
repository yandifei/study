在 HTML 中，`<body>` 标签是定义**文档主体内容**的核心容器。它包含了所有呈现给用户的可见内容，是网页结构的核心部分。

**核心总结：**

1.  **位置：** 位于 `<html>` 标签内部，紧跟在 `<head>` 标签之后。
2.  **唯一性：** 一个 HTML 文档中**有且仅有一个** `<body>` 标签。
3.  **内容容器：** 所有需要在浏览器窗口中显示给用户的内容都必须放在 `<body>` 标签内。
4.  **可见元素：** 包含文本、图像、链接、列表、表格、表单、音频、视频、各种布局容器（`<div>`, `<section>`等）以及其他所有用户可交互或看到的元素。
5.  **样式和脚本的挂载点：** CSS 样式经常作用于 `<body>` 或其内部的元素。JavaScript 也常操作 `<body>` 内的元素来实现动态效果和交互。
6.  **属性：**
    *   **全局属性：** 支持所有 HTML 全局属性（如 `id`, `class`, `style`, `title`, `lang`, `dir` 等）。
    *   **事件处理属性 (已不推荐，建议用 JS)：** 支持各种事件处理属性（如 `onload`, `onunload`, `onclick`, `onmousemove`, `onkeydown` 等），用于在特定事件发生时执行脚本。现代开发更推荐使用 JavaScript 的 `addEventListener`。
7.  **渲染流程：** 浏览器在解析 HTML 时，会构建 DOM 树，`<body>` 元素是 DOM 树中表示可见内容部分的根节点（实际根节点是 `<html>`，但可见内容根在 `<body>`）。

**常见包含在 `<body>` 中的标签 (示例)：**

*   **文本与标题：** `<h1>` 到 `<h6>`, `<p>`, `<span>`, `<br>`, `<hr>`
*   **媒体：** `<img>`, `<audio>`, `<video>`, `<picture>`, `<canvas>`
*   **链接：** `<a>`
*   **列表：** `<ul>`, `<ol>`, `<li>`, `<dl>`, `<dt>`, `<dd>`
*   **表格：** `<table>`, `<tr>`, `<th>`, `<td>`, `<caption>`, `<thead>`, `<tbody>`, `<tfoot>`
*   **表单：** `<form>`, `<input>`, `<textarea>`, `<select>`, `<option>`, `<button>`, `<label>`, `<fieldset>`, `<legend>`
*   **分区/布局：** `<div>`, `<span>`, `<header>`, `<footer>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<aside>`
*   **其他：** `<iframe>`, `<script>` (通常放在底部), `<style>` (也可在 head，但内联样式常见于 body 元素上)

**基本结构示例：**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>网页标题</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <h1>这是一个主标题</h1>
    <p>这是一个段落，包含可见的文本内容。</p>
    <img src="image.jpg" alt="描述图片">
    <a href="https://www.example.com">这是一个链接</a>
    <!-- 所有用户可见的内容都在这里 -->
    <script src="script.js"></script>
</body>
</html>
```

**关键点强调：**

*   `<body>` 是 **网页实际内容** 的家。
*   它与 `<head>` 明确分工：`<head>` 包含元数据和资源链接（标题、字符集、样式表、脚本链接等），`<body>` 包含要显示的内容。
*   理解 `<body>` 的范围对于正确应用 CSS 样式和编写操作 DOM 的 JavaScript 至关重要。

**简单来说：`<body>` 标签就是包裹着你打开网页时在浏览器窗口里看到的所有东西的那个大盒子。**