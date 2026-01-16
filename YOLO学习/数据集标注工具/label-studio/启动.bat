@echo off
title Label Studio 启动器
echo 正在启动 Label Studio，请稍候...
echo 启动成功后，请在浏览器访问 http://localhost:8080
echo.

:: 检查是否安装了 label-studio
where label-studio >nul 2>nul
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Label Studio，正在尝试为你安装...
    pip install label-studio
)

:: 启动服务
label-studio
pause