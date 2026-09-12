@echo off
title MongoDB Sharded Cluster - Full Startup (4 nodes each)
cd /d "%~dp0"

echo ========================================
echo 启动 MongoDB 分片集群（4节点副本集）
echo ========================================

REM 1. 配置服务器 (4个)
echo [1/4] 启动配置服务器 (27019-27022)...
start "Config1-27019" .\mongod.exe --config config\config1.conf
start "Config2-27020" .\mongod.exe --config config\config2.conf
start "Config3-27021" .\mongod.exe --config config\config3.conf
start "Config4-27022" .\mongod.exe --config config\config4.conf

REM 2. 分片1 (4个)
echo [2/4] 启动分片1 (37017-37020)...
start "Shard11-37017" .\mongod.exe --config config\shard11.conf
start "Shard12-37018" .\mongod.exe --config config\shard12.conf
start "Shard13-37019" .\mongod.exe --config config\shard13.conf
start "Shard14-37020" .\mongod.exe --config config\shard14.conf

REM 3. 分片2 (4个)
echo [3/4] 启动分片2 (47017-47020)...
start "Shard21-47017" .\mongod.exe --config config\shard21.conf
start "Shard22-47018" .\mongod.exe --config config\shard22.conf
start "Shard23-47019" .\mongod.exe --config config\shard23.conf
start "Shard24-47020" .\mongod.exe --config config\shard24.conf

REM 4. 路由服务器
echo [4/4] 启动路由服务器 (27018)...
start "Mongos-27018" .\mongos.exe --config config\mongos.conf

echo ========================================
echo 所有节点已启动！
echo 连接路由: mongosh --port 27018
echo 关闭对应窗口即可停止服务
echo ========================================