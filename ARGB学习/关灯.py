# 自带的包
import os
import socket
import subprocess
import threading
import time
# 第三方包
from openrgb import OpenRGBClient

# OpenRGB的绝对路径(当前路径和相对路径拼接)
OpenRGB_path =  os.path.join(os.getcwd(),"OpenRGB Windows 64-bit","OpenRGB.exe")

def start_server():
    """启动OpenRGB的服务端"""
    # 执行命令启动服务并获取输出(非流式)
    result = subprocess.run(
        # 命令列表（避免注入风险）
        [OpenRGB_path, "--server","--server-port", "6742", "--profile", "default"],
        capture_output=True,   # 捕获输出
        text=True,             # 返回字符串
        check=True             # 检查错误（非零退出码抛异常）
    )
    print(result.stdout)

# 检查是否开启了服务器
try:
    socket.create_connection(("localhost", 6742), timeout=1)
except (socket.error, socket.timeout):
    start_server()  # 启动OpenRGB的服务端
    time.sleep(5)  # 等待服务器初始化
    print("OpenRGB的服务端已启动")




# 实例化对象
cli = OpenRGBClient()
cli.clear()  # 关闭所有灯光
