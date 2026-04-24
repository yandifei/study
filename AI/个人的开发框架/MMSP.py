"""MMSP.py
程序主入口
最优先加载日志记录器
"""
# 内置库
import asyncio
import os
import signal
from contextlib import asynccontextmanager
from typing import Literal
import webbrowser
# 三方库
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
# 自己的模块
from logger import logger_manager, info, critical, warning  # 导入日志记录器模块
from utils.config_manager import ConfigManager # 导入配置管理模块
from utils.path_utils import get_root
from utils.qrcode_manager import get_local_ip, QRCodeManager

"""初始化"""
# 是否为开发模式
# debug = True
debug = False
# 版本
VERSION: str = "1.0.0"
# 创建配置管理器实例（这是个单例）
config_manager = ConfigManager(debug=debug)
info("日志模块加载完成，全局异常捕获开启")
# 层叠覆盖原来的配置
config_manager.config_override()  # 层叠覆盖原来的配置
info("层叠覆盖原来的配置完成")
# 协议
PROTOCOL: str = config_manager.config_data.server.protocol
# 主机号
HOST: str = config_manager.config_data.server.host
# 端口号
PORT: int = config_manager.config_data.server.port
info(f"服务器配置，协议：{PROTOCOL}，主机：{HOST}，端口：{PORT}")

"""生命周期自动管理"""
@asynccontextmanager
async def lifespan(app: FastAPI):
    """使用异步生命周期管理"""
    # 创建   工厂实例

    # 共享变量
    # app.state.playwright_factory = playwright_factory
    # 打印服务器信息并打开浏览器
    if HOST == "0.0.0.0":
        info(f"浏览器请访问：{PROTOCOL}://localhost:{PORT}")
        webbrowser.open(f"{PROTOCOL}://localhost:{PORT}") # 打开用户本地浏览器
        QRCodeManager().create_qrcode(f"{PROTOCOL}://{get_local_ip()}:{PORT}")  # 创建二维码
    else:
        info(f"浏览器请访问：{PROTOCOL}://{HOST}:{PORT}")
        webbrowser.open(f"{PROTOCOL}://{HOST}:{PORT}")  # 打开用户本地浏览器
    """干活"""
    yield
    """资源释放"""
    # 关闭 工厂实例（手动好看，但也能自动管理的）
    info("资源释放")

# 创建FastAPI实例（创建后才进行路由注册）
app = FastAPI(lifespan=lifespan)
# 关键：将硬盘目录映射到网络路径 "/outputs"
app.mount("/outputs", StaticFiles(directory=get_root() / "outputs"), name="outputs")
# 挂载整个 template 目录到 /template 路径下
app.mount("/templates", StaticFiles(directory=get_root() / "templates"), name="templates")




if __name__ == "__main__":
    # 2021.03.25是爱丽丝的生日
    uvicorn.run(app, host=HOST, port=PORT)
