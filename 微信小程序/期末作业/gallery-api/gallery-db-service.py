"""WebAIPilot.py
程序主入口
优先加载日志记录器
"""
# 内置库
import webbrowser
import os
import signal
from contextlib import asynccontextmanager
from datetime import datetime, timezone
# 三方库
import uvicorn
from fastapi import FastAPI, Request, Query
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
# 自己的模块
from logger import info, warning  # 导入日志记录器模块
from utils.config_manager import ConfigManager # 导入配置管理模块
from utils.path_utils import get_root
from services.auth import auth_router  # 认证路由
from services.browse import browse_router  # 浏览记录路由
from services.favorite import favorite_router  # 收藏记录路由
from services.auth.jwt import (        # 自定义异常 + 全局异常处理
    TokenExpiredError,
    TokenInvalidError,
    TokenMissingError,
    TokenTypeError,
    InsufficientPermissionError,
)
from services.database import init_db, close_db  # MongoDB 生命周期管理
from services.database.redis import redis_client
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
    mongo_client = None
    try:
        mongo_client, _ = await init_db()
    except Exception as e:
        warning(f"MongoDB 连接失败，持久数据库将不可以使用: {e}")

    # # 存储在应用程序的状态
    # app.state.config_manager = config_manager
    # app.state.playwright_factory = playwright_factory
    # app.state.ai_task_flows = ai_task_flows
    """干活"""
    yield
    """资源释放"""
    # 关闭 MongoDB 连接
    if mongo_client:
        await close_db(mongo_client)
    # 2. 应用关闭时：必须优雅地关闭连接池
    await redis_client.aclose()  # 注意：新版本 redis-py 建议使用 aclose() 替代 close()

# 创建FastAPI实例（创建后才进行路由注册）
app = FastAPI(lifespan=lifespan)
# 将硬盘目录映射到网络路径 "/outputs"来访问日志
app.mount("/outputs", StaticFiles(directory=get_root() / "outputs"), name="outputs")
# 将管理面板静态资源（CSS/JS）映射到网络路径
app.mount("/static/admin", StaticFiles(directory=get_root() / "templates" / "index"), name="admin_static")
# ============================================================================
#  注册认证路由
# ============================================================================
app.include_router(auth_router)
app.include_router(browse_router)
app.include_router(favorite_router)

# ============================================================================
#  管理面板 API
# ============================================================================

"""日志文件路径映射"""
LOG_FILES = {
    "error": get_root() / "outputs" / "logs" / "error.log",
    "running": get_root() / "outputs" / "logs" / "日志记录.log",
}


def _read_log_tail(file_path, lines: int = 15) -> str:
    """读取日志文件的最后 N 行"""
    if not file_path.exists():
        return ""
    try:
        text = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = file_path.read_text(encoding="gbk")
    all_lines = text.splitlines()
    return "\n".join(all_lines[-lines:])


def _read_log_full(file_path):
    """读取完整日志文件，返回 (content, line_count, size)"""
    if not file_path.exists():
        return "", 0, 0
    try:
        text = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = file_path.read_text(encoding="gbk")
    return text, text.count("\n") + (1 if text else 0), file_path.stat().st_size


@app.get("/api/admin/logs/preview")
async def admin_log_preview(type: str = Query(..., description="日志类型: error | running"), lines: int = Query(15, ge=1, le=200)):
    """获取日志预览（最后 N 行）"""
    file_path = LOG_FILES.get(type)
    if file_path is None:
        return JSONResponse(status_code=400, content={"error": f"未知日志类型: {type}，可选: error, running"})
    content = _read_log_tail(file_path, lines)
    return {"type": type, "lines": lines, "content": content}


@app.get("/api/admin/logs/full")
async def admin_log_full(type: str = Query(..., description="日志类型: error | running")):
    """获取完整日志内容"""
    file_path = LOG_FILES.get(type)
    if file_path is None:
        return JSONResponse(status_code=400, content={"error": f"未知日志类型: {type}，可选: error, running"})
    content, line_count, size = _read_log_full(file_path)
    return {"type": type, "content": content, "line_count": line_count, "size": size}


@app.get("/api/admin/info")
async def admin_server_info():
    """获取服务器运行信息"""
    return {
        "host": HOST,
        "port": PORT,
        "protocol": PROTOCOL,
        "start_time": SERVER_START_TIME,
        "app_name": os.getenv("APP_NAME", "mongodb_service"),
    }


@app.get("/api/admin/health")
async def admin_health_check():
    """健康检查（供前端轮询服务状态）"""
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}

# ============================================================================
#  系统接口
# ============================================================================

# 首页 —— 后端管理面板
@app.get("/", response_class=HTMLResponse)
async def admin_dashboard():
    """后端管理面板首页"""
    html_path = get_root() / "templates" / "index" / "index.html"
    if html_path.exists():
        return html_path.read_text(encoding="utf-8")
    return HTMLResponse("<h1>管理面板文件未找到</h1>", status_code=404)


# 关闭服务 DELETE 端点
@app.delete("/{password}")
async def shutdown_server(password: str):
    """通过密码关闭 FastAPI 服务"""
    expected = os.environ.get("EXIT_PASSWORD", "")
    if expected and password == expected:
        info("收到合法的关闭指令，正在停止服务...")
        os.kill(os.getpid(), signal.SIGINT)
        return {"message": "程序已关闭"}
    else:
        return JSONResponse(
            status_code=403,
            content={"error": "密码错误或未配置 EXIT_PASSWORD 环境变量"},
        )

# 图标
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(get_root() / "config" / "logo.ico")

"""认证异常处理器"""
@app.exception_handler(TokenExpiredError)
async def token_expired_handler(request, exc: TokenExpiredError):
    """Token 过期 → 401"""
    return JSONResponse(
        status_code=401,
        content={"code": 401, "msg": exc.message, "data": None},
        headers={"X-Token-Error": "expired"},
    )
@app.exception_handler(TokenInvalidError)
async def token_invalid_handler(request, exc: TokenInvalidError):
    """Token 无效 → 401"""
    return JSONResponse(
        status_code=401,
        content={"code": 401, "msg": exc.message, "data": None},
        headers={"X-Token-Error": "invalid"},
    )

@app.exception_handler(TokenMissingError)
async def token_missing_handler(request, exc: TokenMissingError):
    """Token 缺失 → 401"""
    return JSONResponse(
        status_code=401,
        content={"code": 401, "msg": exc.message, "data": None},
    )

@app.exception_handler(TokenTypeError)
async def token_type_error_handler(request, exc: TokenTypeError):
    """Token 类型错误 → 401"""
    return JSONResponse(
        status_code=401,
        content={"code": 401, "msg": exc.message, "data": None},
        headers={"X-Token-Error": "wrong-type"},
    )

@app.exception_handler(InsufficientPermissionError)
async def permission_error_handler(request, exc: InsufficientPermissionError):
    """权限不足 → 403"""
    return JSONResponse(
        status_code=403,
        content={"code": 403, "msg": exc.message, "data": None},
    )


if __name__ == "__main__":
    # 2021.03.25是爱丽丝的生日
    uvicorn.run(app, host=HOST, port=PORT)