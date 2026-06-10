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
from services.auth import auth_router  # 认证路由
from services.auth.jwt import (        # 自定义异常 + 全局异常处理
    AuthException,
    TokenExpiredError,
    TokenInvalidError,
    TokenMissingError,
    TokenTypeError,
    InsufficientPermissionError,
)
from services.database import init_db, close_db  # MongoDB 生命周期管理
from services.database.redis import redis_client

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

# ============================================================================
#  注册认证路由
# ============================================================================
app.include_router(auth_router)

# ============================================================================
#  全局异常处理器 —— 将自定义认证异常映射为 HTTP 响应
#  企业实践: 异常处理器统一管理错误响应格式，保持 API 一致性
# ============================================================================

# 图标
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(get_root() / "config" / "logo.ico")

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

# 关键：将硬盘目录映射到网络路径 "/outputs"
app.mount("/outputs", StaticFiles(directory=get_root() / "outputs"), name="outputs")


if __name__ == "__main__":
    # 2021.03.25是爱丽丝的生日
    uvicorn.run(app, host=HOST, port=PORT)