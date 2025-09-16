<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>炫酷9x9乘法口诀表</title>
    <style>
        /* 重置默认样式 */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Arial Rounded MT Bold', 'Segoe UI', sans-serif;
        }

        /* 页面整体样式 */
        body {
            /* 创建渐变背景 */
            background: linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d);
            min-height: 100vh; /* 确保背景覆盖整个屏幕高度 */
            display: flex;
            justify-content: center; /* 水平居中 */
            align-items: center; /* 垂直居中 */
            padding: 20px; /* 添加内边距 */
        }

        /* 主容器样式 */
        .container {
            text-align: center;
            max-width: 1200px; /* 最大宽度限制 */
            width: 100%; /* 响应式宽度 */
        }

        /* 标题样式 */
        h1 {
            color: white;
            font-size: 2.8rem;
            margin-bottom: 30px;
            text-shadow: 0 0 15px rgba(255, 255, 255, 0.7); /* 文字发光效果 */
            letter-spacing: 2px; /* 字母间距 */
        }

        /* 乘法表网格容器 */
        .multiplication-table {
            display: grid;
            grid-template-columns: repeat(9, 1fr); /* 创建9列等宽网格 */
            gap: 15px; /* 网格间距 */
            perspective: 1000px; /* 3D透视效果 */
        }

        /* 单元格基础样式 */
        .cell {
            background: rgba(255, 255, 255, 0.1); /* 半透明背景 */
            backdrop-filter: blur(10px); /* 背景模糊效果 */
            border-radius: 12px; /* 圆角 */
            padding: 15px 5px;
            color: white;
            font-size: 1.2rem;
            display: flex;
            justify-content: center;
            align-items: center;
            aspect-ratio: 1; /* 保持正方形 */
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37); /* 阴影效果 */
            border: 1px solid rgba(255, 255, 255, 0.18); /* 半透明边框 */
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); /* 平滑过渡动画 */
            transform-style: preserve-3d; /* 保持3D变换 */
            cursor: pointer; /* 指针光标 */
            position: relative;
            overflow: hidden;
        }

        /* 单元格光泽效果（伪元素） */
        .cell:before {
            content: "";
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(
                45deg,
                rgba(255, 255, 255, 0) 0%,
                rgba(255, 255, 255, 0.1) 50%,
                rgba(255, 255, 255, 0) 100%
            );
            transform: rotate(45deg);
            transition: all 0.5s;
        }

        /* 单元格悬停效果 */
        .cell:hover {
            transform: translateY(-10px) rotate3d(1, 1, 0, 10deg); /* 上浮和3D旋转 */
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5); /* 增强阴影 */
            background: rgba(255, 255, 255, 0.2); /* 背景变亮 */
        }

        /* 悬停时光泽动画 */
        .cell:hover:before {
            transform: rotate(45deg) translate(20%, 20%);
        }

        /* 表头单元格特殊样式 */
        .header {
            background: linear-gradient(135deg, #ff6b6b, #ff8e53); /* 渐变背景 */
            font-weight: bold;
            font-size: 1.4rem;
            transform: rotate3d(1, 1, 1, 10deg); /* 初始3D旋转 */
            box-shadow: 0 10px 30px rgba(255, 107, 107, 0.4); /* 特殊阴影 */
        }

        /* 对角线单元格特殊样式 */
        .diagonal {
            background: linear-gradient(135deg, #4ecdc4, #556270); /* 不同渐变 */
            font-weight: bold;
            transform: scale(1.05); /* 稍微放大 */
            box-shadow: 0 10px 30px rgba(78, 205, 196, 0.4); /* 特殊阴影 */
        }

        /* 中等屏幕响应式设计 */
        @media (max-width: 1200px) {
            .multiplication-table {
                grid-template-columns: repeat(5, 1fr); /* 改为5列 */
            }

            h1 {
                font-size: 2.2rem; /* 标题缩小 */
            }

            .cell {
                font-size: 1rem; /* 字体缩小 */
                padding: 10px 3px; /* 内边距调整 */
            }
        }

        /* 小屏幕响应式设计 */
        @media (max-width: 768px) {
            .multiplication-table {
                grid-template-columns: repeat(3, 1fr); /* 改为3列 */
                gap: 10px; /* 间距缩小 */
            }

            h1 {
                font-size: 1.8rem; /* 标题进一步缩小 */
            }

            .cell {
                font-size: 0.9rem; /* 字体进一步缩小 */
                padding: 8px 2px; /* 内边距进一步调整 */
            }
        }

        /* 底部提示文字样式 */
        .glow {
            text-align: center;
            margin-top: 40px;
            color: white;
            font-size: 1.2rem;
            animation: pulse 2s infinite; /* 脉冲动画 */
        }

        /* 脉冲动画关键帧 */
        @keyframes pulse {
            0% { opacity: 0.7; }
            50% { opacity: 1; text-shadow: 0 0 15px rgba(255, 255, 255, 0.9); }
            100% { opacity: 0.7; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>炫酷9x9乘法口诀表</h1>

        <div class="multiplication-table">
            <%-- 乘法表左上角空单元格 --%>
            <div class="cell header">×</div>

            <%-- 生成列标题(1-9) --%>
            <% for(int i = 1; i <= 9; i++) { %>
                <div class="cell header"><%= i %></div>
            <% } %>

            <%-- 生成乘法表数据行 --%>
            <% for(int i = 1; i <= 9; i++) { %>
                <%-- 行标题 --%>
                <div class="cell header"><%= i %></div>

                <%-- 生成当前行的数据单元格 --%>
                <% for(int j = 1; j <= 9; j++) { %>
                    <%-- 对角线上的单元格使用特殊样式 --%>
                    <% if(i == j) { %>
                        <div class="cell diagonal"><%= i %> × <%= j %> = <%= i*j %></div>
                    <% } else { %>
                        <div class="cell"><%= i %> × <%= j %> = <%= i*j %></div>
                    <% } %>
                <% } %>
            <% } %>
        </div>

        <div class="glow">悬停在单元格上查看炫酷效果</div>
    </div>
</body>
</html>