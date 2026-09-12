<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html>
<head>
    <title>English Alphabet</title>
    <style>
        body {
            background: #6a11cb; /* 使用纯色背景替代图片 */
            background: linear-gradient(to right, #6a11cb, #2575fc); /* 渐变背景 */
            font-family: Arial, sans-serif; /* 使用通用字体 */
        }
        .title {
            font-family: "Microsoft YaHei", "SimHei", sans-serif; /* 更通用的中文字体 */
            font-size: 36px;
            text-align: center;
            margin-top: 20px;
        }
        .alphabet {
            font-family: "Microsoft YaHei", "SimSun", serif; /* 更通用的中文字体 */
            font-size: 25px;
            color: blue;
            text-align: center;
            line-height: 1.8;
            margin: 20px auto;
            max-width: 800px;
        }
    </style>
</head>
<body>
    <p class="title">
        <br>英文字母表
    </p>

    <p class="alphabet">
        <%
            // Loop from 'A' to 'Z'
            for (char upperCase = 'A'; upperCase <= 'Z'; upperCase++) {
                // Calculate the corresponding lowercase letter
                char lowerCase = (char) (upperCase + 32);

                // Print the pair, e.g., A(a)
                out.print(upperCase + "(" + lowerCase + ") ");

                // After printing 'M', insert a line break
                if (upperCase == 'M') {
                    out.print("<br>");
                }
            }
        %>
    </p>
</body>
</html>