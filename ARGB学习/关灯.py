# 自带的包
import os
import subprocess
import threading
import time
# 第三方包
from openrgb import OpenRGBClient


OpenRGB_path =  os.path.join(os.getcwd(),"OpenRGB Windows 64-bit","OpenRGB.exe")  # OpenRGB的绝对路径(当前路径和相对路径拼接)
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

try:
    start_server_thread = threading.Thread(target=start_server, daemon=True) # 创建启动OpenRGB的服务的线程(守护线程：设置 daemon=True 使线程随主线程结束)
    start_server_thread.start()  # 启动线程
    time.sleep(10)  # 等待服务器初始化
except IndexError:
    print("OpenRGB的服务端已启动")

# 实例化对象
cli = OpenRGBClient()
cli.clear()  # 关闭所有灯光
