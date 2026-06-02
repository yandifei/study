@echo off
setlocal enabledelayedexpansion

:: 1. 停止 MongoDB 相关进程
echo [1/3] 正在停止 MongoDB 进程...
taskkill /f /im mongod.exe /t >nul 2>&1
taskkill /f /im mongos.exe /t >nul 2>&1

:: 2. 定义目录列表
set "nodes=config1 config2 config3 config4 shard11 shard12 shard13 shard14 shard21 shard22 shard23 shard24"

echo [2/3] 正在清空并重建数据与日志目录...

:: 3. 循环遍历并处理
for %%i in (%nodes%) do (
    :: 处理 data 目录
    if exist "data\%%i" (
        echo   - 清空 data\%%i
        rmdir /s /q "data\%%i"
        mkdir "data\%%i"
    )
    
    :: 处理 logs 目录
    if exist "logs\%%i" (
        echo   - 清空 logs\%%i
        rmdir /s /q "logs\%%i"
        mkdir "logs\%%i"
    )
)

:: 处理 mongos 日志目录
if exist "logs\mongos" (
    echo   - 清空 logs\mongos
    rmdir /s /q "logs\mongos"
    mkdir "logs\mongos"
)

echo [3/3] 重置完成。
echo ========================================