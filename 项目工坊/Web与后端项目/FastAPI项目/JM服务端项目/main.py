"""MMSP.py
程序主入口
最优先加载日志记录器
"""
# 内置库
import os
import signal
import threading
from contextlib import asynccontextmanager
import webbrowser
from uuid import uuid4
# 三方库
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, BackgroundTasks, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

# 自己的模块
from logger import logger_manager, info, critical, warning  # 导入日志记录器模块
from service.jm_down import download_jmcomic
from utils.config_manager import ConfigManager # 导入配置管理模块
from utils.path_utils import get_root
from utils.qrcode_manager import get_local_ip, QRCodeManager
from service import jm_down

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
# 存储任务状态（简单内存版，生产环境建议用 Redis）

# 创建FastAPI实例（创建后才进行路由注册）
app = FastAPI(lifespan=lifespan)
# 关键：将硬盘目录映射到网络路径 "/outputs"
app.mount("/outputs", StaticFiles(directory=get_root() / "outputs"), name="outputs")
# 存储任务（简单内存版，生产环境用 Redis）
tasks = {}
lock = threading.Lock()

"""系统接口"""
@app.post("/")
@app.get("/")
async def index_html(request: Request):
    if request.method == "GET":
        return {"version": VERSION, "message": "当前状态良好"}
    elif request.method == "POST":
        return {"version": VERSION}
    else:
        return {"error": "使用了错误的请求方法"}

# @app.get("/favicon.ico")
# async def favicon():
#     return FileResponse(get_root()/ "config" / "1.ico")

# 关闭程序接口
@app.delete("/close")
async def close(request: Request):
    if request.method == "DELETE":
        # task_core: TaskCore = app.state.task_core
        # task_core.run_flag = False  # 设置停止标志位（防止退出崩溃）
        info("执行清理资源代码，清理完后关闭程序")
        # 获取当前进程ID,然后关闭进程，触发回收方法
        # SIGINT 相当于键盘上的 Ctrl+C，能触发 Uvicorn 的回收清理机制
        # 关闭Playwright工厂实例（手动好看，但也能自动管理的）
        os.kill(os.getpid(), signal.SIGINT)  # 告知系统：“该进程是被用户中断指令关闭的”。
        return {"message": "程序已关闭"}
    else:
        return {"error": "使用了错误的请求方法"}

# # 获取图片链接接口
# @app.get("/outputs/下载缓存/{album_id}")
# async def get_jm_img_link(album_id: str):
#     return FileResponse(
#         path=f"/outputs/下载缓存/{album_id}",
#         media_type="text/plain",
#         headers={"Content-Disposition": f"inline; filename*=UTF-8''{filename}"}
#     )

def process_download(album_id: str):
    """同步后台任务，在线程中执行"""
    try:
        msg, status = download_jmcomic(album_id)
        with lock:
            if status is not None: tasks[album_id]["status"] = status
            tasks[album_id]["message"] = msg
    except Exception as e:
        with lock:
            tasks[album_id]["status"] = False
            tasks[album_id]["message"] = str(e)


@app.post("/download/{album_id}")
async def start_download_jmcomic(album_id: str, background_tasks: BackgroundTasks):
    tasks[album_id] = {
        "album_id": album_id,
        "status": None,
        "message": f"开始下载 {album_id}",
    }
    background_tasks.add_task(process_download, album_id)
    return tasks[album_id]

@app.get("/download/status/{task_id}")
async def get_download_status(task_id: str):
    """查询下载任务状态"""
    task = tasks.get(task_id)
    if not task:
        return {"message": "任务不存在"}
    # 返回任务信息（通过status判断任务是否完成）
    if task["status"] is False:
        return {"message": "任务还没有完成"}
    else:
        files = os.listdir(f"outputs/下载缓存/{task["album_id"]}")
        links = [] 
        for file in files:
            links.append(f"outputs/下载缓存/{task['album_id']}/{file}")
    return {"message": links}


# 获取日志（这里本来我不用写的，结果浏览器乱解析编码格式，即使我在html里面写了utf-8）
@app.get("/outputs/logs/{filename}")
async def get_log(filename: str):
    return FileResponse(
        path=f"outputs/logs/{filename}",
        media_type="text/plain",
        headers={"Content-Disposition": f"inline; filename*=UTF-8''{filename}"}
    )

if __name__ == "__main__":
    # 2021.03.25是爱丽丝的生日
    uvicorn.run(app, host=HOST, port=PORT)
