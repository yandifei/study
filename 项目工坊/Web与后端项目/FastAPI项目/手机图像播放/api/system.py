"""system.py
提供系统级别的api服务
"""
import os
import platform
import psutil
from datetime import datetime
from typing import Dict, Any
from fastapi import APIRouter

router = APIRouter(prefix="/sys", tags=["sys"])

@router.get("/")
async def get_system_info() -> Dict[str, Any]:
    """
    获取系统和硬件信息
    
    Returns:
        包含系统信息的字典
    """
    try:
        # 系统基本信息
        system_info = {
            "system": {
                "platform": platform.system(),
                "platform_version": platform.version(),
                "platform_release": platform.release(),
                "architecture": platform.machine(),
                "hostname": platform.node(),
                "python_version": platform.python_version(),
                "python_compiler": platform.python_compiler(),
                "uptime": str(datetime.now() - datetime.fromtimestamp(psutil.boot_time()))
            },
            
            # CPU信息
            "cpu": {
                "physical_cores": psutil.cpu_count(logical=False),
                "total_cores": psutil.cpu_count(logical=True),
                "max_frequency": f"{psutil.cpu_freq().max:.2f}Mhz" if psutil.cpu_freq() else "Unknown",
                "current_frequency": f"{psutil.cpu_freq().current:.2f}Mhz" if psutil.cpu_freq() else "Unknown",
                "cpu_usage_per_core": [f"{percentage}%" for percentage in psutil.cpu_percent(percpu=True, interval=1)],
                "total_cpu_usage": f"{psutil.cpu_percent(interval=1)}%"
            },
            
            # 内存信息
            "memory": {
                "total_memory": f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
                "available_memory": f"{psutil.virtual_memory().available / (1024**3):.2f} GB",
                "used_memory": f"{psutil.virtual_memory().used / (1024**3):.2f} GB",
                "memory_percentage": f"{psutil.virtual_memory().percent}%"
            },
            
            # 磁盘信息
            "disk": {},
            
            # 网络信息
            "network": {
                "bytes_sent": f"{psutil.net_io_counters().bytes_sent / (1024**2):.2f} MB",
                "bytes_received": f"{psutil.net_io_counters().bytes_recv / (1024**2):.2f} MB"
            }
        }
        
        # 获取磁盘分区信息
        partitions = psutil.disk_partitions()
        for partition in partitions:
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
                system_info["disk"][partition.device] = {
                    "mountpoint": partition.mountpoint,
                    "file_system_type": partition.fstype,
                    "total_size": f"{partition_usage.total / (1024**3):.2f} GB",
                    "used": f"{partition_usage.used / (1024**3):.2f} GB",
                    "free": f"{partition_usage.free / (1024**3):.2f} GB",
                    "percentage": f"{partition_usage.percent}%"
                }
            except PermissionError:
                # 处理无权限访问的分区
                system_info["disk"][partition.device] = {
                    "mountpoint": partition.mountpoint,
                    "error": "Permission denied"
                }
        
        return system_info
        
    except Exception as e:
        return {"error": f"Failed to retrieve system information: {str(e)}"}

@router.get("/health")
async def health_check() -> Dict[str, str]:
    """
    健康检查端点
    
    Returns:
        健康状态信息
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "System API"
    }

@router.get("/processes")
async def get_processes(limit: int = 10) -> Dict[str, Any]:
    """
    获取运行中的进程信息
    
    Args:
        limit: 返回的进程数量限制
        
    Returns:
        进程列表
    """
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_percent', 'cpu_percent']):
            try:
                process_info = proc.info
                # 过滤掉内存和CPU使用率为None的进程
                if process_info['memory_percent'] is not None and process_info['cpu_percent'] is not None:
                    processes.append({
                        "pid": process_info['pid'],
                        "name": process_info['name'],
                        "username": process_info['username'],
                        "memory_usage": f"{process_info['memory_percent']:.2f}%",
                        "cpu_usage": f"{process_info['cpu_percent']:.2f}%"
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
        # 按内存使用率排序并限制数量
        processes.sort(key=lambda x: float(x['memory_usage'].rstrip('%')), reverse=True)
        return {"processes": processes[:limit]}
        
    except Exception as e:
        return {"error": f"Failed to retrieve process information: {str(e)}"}