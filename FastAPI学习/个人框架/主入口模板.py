"""主入口模板.py
程序主入口
优先加载日志记录器
"""
# 内置库
import webbrowser
from contextlib import asynccontextmanager
from datetime import datetime, timezone
# 三方库
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
# 自己的模块
from logger import info, warning  # 导入日志记录器模块
from utils.config_manager import ConfigManager # 导入配置管理模块
from utils.path_utils import get_root
from utils.qrcode_manager import QRCodeManager, get_local_ip

"""初始化"""
# 是否为开发模式
debug = False
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
SERVER_START_TIME = datetime.now(timezone.utc).isoformat()
info(f"服务器配置，协议：{PROTOCOL}，主机：{HOST}，端口：{PORT}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """使用异步生命周期管理"""
    # 打印服务器信息并打开浏览器
    if HOST == "0.0.0.0":
        info(f"浏览器请访问：{PROTOCOL}://localhost:{PORT}")
        webbrowser.open(f"{PROTOCOL}://localhost:{PORT}")  # 打开用户本地浏览器
        QRCodeManager().create_qrcode(f"{PROTOCOL}://{get_local_ip()}:{PORT}")  # 创建二维码
    else:
        info(f"浏览器请访问：{PROTOCOL}://{HOST}:{PORT}")
        webbrowser.open(f"{PROTOCOL}://{HOST}:{PORT}")  # 打开用户本地浏览器
    # ── MongoDB 初始化（认证模块依赖） ──

    # # 存储在应用程序的状态
    # app.state.config_manager = config_manager
    # app.state.playwright_factory = playwright_factory
    # app.state.ai_task_flows = ai_task_flows
    """干活"""
    yield
    """资源释放"""

# 创建FastAPI实例（创建后才进行路由注册）
app = FastAPI(lifespan=lifespan)
# 将硬盘目录映射到网络路径 "/outputs"来访问日志
app.mount("/outputs", StaticFiles(directory=get_root() / "outputs"), name="outputs")
# 将管理面板静态资源（CSS/JS）映射到网络路径
app.mount("/templates", StaticFiles(directory=get_root() / "templates"), name="templates")

"""系统接口"""
@app.get("/")
def index():
    return JSONResponse(
        content={
        "服务器状态": "运行正常",
        "服务": "ERP监控告警系统",
        "版本": "1.0.0"
        },
        headers={"Content-Type": "application/json; charset=utf-8"}
    )

@app.get("/favicon.ico")
async def favicon():
    return FileResponse(get_root()/ "config" / "logo.ico")

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)