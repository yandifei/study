"""WebAIPilot.py
程序主入口
优先加载日志记录器
"""
# 内置库
import warnings
from contextlib import asynccontextmanager
# 三方库
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

import utils.path_utils
from requests_model import AskModel
# 自己的模块
from utils import logger_manager, info, critical    # 导入日志记录器模块
from utils import ConfigManager # 导入配置管理模块
from utils.path_utils import get_root
from utils.playwright_factory.playwright_factory import PlaywrightFactory
from logic.doubao_logic.doubao_flows import DoubaoFlows

# # 忽略 asyncio 关于未关闭传输的 ResourceWarning（工厂会自动回收资源）
# warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed transport")
# warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed event loop")

# 协议
PROTOCOL = "http"
# 主机号
HOST = "127.0.0.1"
# 端口号
PORT = 21325

@asynccontextmanager
async def lifespan(app: FastAPI):
    """使用异步生命周期管理"""
    """初始化"""
    # 创建配置管理器实例（这是个单例）
    config_manager = ConfigManager(debug=True)
    # 层叠覆盖原来的日志配置
    config_manager.config_override()  # 层叠覆盖原来的配置
    info("日志模块加载完成，全局异常捕获开启")
    # 创建Playwright工厂实例
    playwright_factory = PlaywrightFactory(config_manager.config_data["playwright"]["launch_options"],config_manager.config_data["playwright"]["context_options"])
    # 创建豆包工作流实例
    doubao_flows =  await DoubaoFlows.create(config_manager, playwright_factory)
    # 存储在应用程序的状态
    app.state.config_manager = config_manager
    app.state.playwright_factory = playwright_factory
    app.state.doubao_flows = doubao_flows
    """干活"""
    yield
    """资源释放"""
    # 关闭Playwright工厂实例（手动好看，但也能自动管理的）
    await playwright_factory.close_factory()
    info("Playwright工厂已关闭")

# 创建FastAPI实例（创建后才进行路由注册）
app = FastAPI(lifespan=lifespan)
# 关键：将硬盘目录映射到网络路径 "/outputs"
app.mount("/outputs", StaticFiles(directory=get_root() / "outputs"), name="outputs")

@app.get("/")
def index():
    return {
        "服务器状态": "运行正常",
        "服务": "WebAIPilot API",
        "版本": "1.0.0"
    }


@app.get("/screenshots",  response_class=FileResponse)
async def screenshots():
    # 直接从app.state获取对象
    df: DoubaoFlows = app.state.doubao_flows
    await df.home_page.page.screenshot(path=get_root() / "outputs" / "screenshots" / "screenshots.png")
    return FileResponse(path=get_root() / "outputs" / "screenshots" / "screenshots.png")

@app.get("/status",  response_class=HTMLResponse)
async def status():
    # 直接从app.state获取对象
    df: DoubaoFlows = app.state.doubao_flows
    await df.home_page.page.screenshot(path=get_root() / "outputs" / "screenshots" / "status.png")
    html_content = f"""
<html>
<head>
    <title>Playwright 状态监控</title>
    <style>.{{margin: 0;padding: 0px;}}</style>
</head>
<body>
    <img id="status_img" src="{get_root() / "outputs" / "screenshots" / "status.png"}" style="width: 100%; border: 3px solid #000;">
    <script>
        const img = document.getElementById("status_img");
        setInterval(() => {{
            img.src = "{PROTOCOL}://{HOST}:{PORT}/screenshots?t=" + new Date().getTime();
        }}, 33);
    </script>
</body>
</html>
"""
    # img.src = "{PROTOCOL}://{HOST}:{PORT}/screenshots?t=" + new Date().getTime();
    return HTMLResponse(content=html_content)


@app.post("/ask")
async def ask_post(ask_model: AskModel):
    # 直接从app.state获取对象
    df: DoubaoFlows = app.state.doubao_flows
    if ask_model.question == "":
        return {
            "error": "大哥，你输入问题呀"
        }
    # 提问（转成字典并解引用）
    text_answer, img_urls =  await df.home_page.ask(**ask_model.model_dump())

    return {
        "AI回复": text_answer,
        "图片链接": img_urls
    }


if __name__ == "__main__":
    # 2021.03.25是爱丽丝的生日
    uvicorn.run(app, host=HOST, port=PORT)