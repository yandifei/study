@echo off

:: 强制切换到 D 盘 (加上 /d 确保跨盘符跳转成功)
cd /d "D:\YOLO 数据集合\label-studio"

:: 初始化 Conda 并激活环境
:: 注意：如果你的 Miniconda/Anaconda 安装在其他路径，请修改下方的路径
call conda activate yolo-study

:: 把 Label Studio 的运行数据存到 D 盘，防止挤爆 C 盘（缓存在C:\Users\用户名\AppData\Local\label-studio）
set LABEL_STUDIO_BASE_DATA_DIR=D:\YOLO 数据集合\label-studio\BASE_DATA

:: 设置允许访问本地文件系统的环境变量
set LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true

:: 允许访问D盘的所有图片
set LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT=D:\

:: 启动 Label Studio
label-studio start

pause