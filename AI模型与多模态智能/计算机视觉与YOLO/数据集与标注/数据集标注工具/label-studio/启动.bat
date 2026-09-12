@echo off

:: 强制切换到bat目录
cd /d "%~dp0"

:: 确保 base_data 目录存在，防止报错
if not exist "%~dp0base_data" mkdir "%~dp0base_data"

:: 初始化 Conda 并激活环境
:: 注意：如果你的 Miniconda/Anaconda 安装在其他路径，请修改下方的路径
call conda activate yolo-study

:: 把 Label Studio 的运行数据存到当前的base_data目录下，防止挤爆 C 盘（缓存在C:\Users\用户名\AppData\Local\label-studio）
set "LABEL_STUDIO_BASE_DATA_DIR=%~dp0base_data"

:: 设置允许访问本地文件系统的环境变量
set LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true

:: 允许访问脚本所在盘符的整盘文件，提高通用性
set "LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT=%~d0\"

:: 启动 Label Studio
label-studio start

pause