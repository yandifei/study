"""WebAIPilot.py
程序主入口
优先加载日志记录器
"""
# 内置库
import asyncio
import os
import warnings
from contextlib import asynccontextmanager
# 三方库
import uvicorn
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
# 自己的模块
from logger import logger_manager, info, critical, warning  # 导入日志记录器模块
from utils.config_manager import ConfigManager # 导入配置管理模块
from utils.path_utils import get_root


"""初始化"""
# 是否为开发模式
debug = True
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


@asynccontextmanager
async def lifespan(app: FastAPI):
    """使用异步生命周期管理"""
    # # 存储在应用程序的状态
    # app.state.config_manager = config_manager
    # app.state.playwright_factory = playwright_factory
    # app.state.ai_task_flows = ai_task_flows
    """干活"""
    yield
    """资源释放"""

# 创建FastAPI实例（创建后才进行路由注册）
app = FastAPI(lifespan=lifespan)

if __name__ == "__main__":
    # 2021.03.25是爱丽丝的生日
    uvicorn.run(app, host=HOST, port=PORT)