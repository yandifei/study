"""WebAIPilot.py
程序主入口
优先加载日志记录器
"""
# 内置库
import asyncio
from contextlib import asynccontextmanager
# 三方库
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
# 自己的模块
from models import AskModel
from utils import logger_manager, info, critical, warning  # 导入日志记录器模块
from utils import ConfigManager # 导入配置管理模块
from utils.path_utils import get_root
from utils.playwright_factory.playwright_factory import PlaywrightFactory
from logic.doubao_logic.doubao_flows import DoubaoFlows
from logic.deepseek_logic.deepseek_flows import DeepseekFlows
from logic.skywork_logic.skywork_flows import SkyworkFlows

# # 忽略 asyncio 关于未关闭传输的 ResourceWarning（工厂会自动回收资源）
# warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed transport")
# warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed event loop")

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
PROTOCOL: str = config_manager.config_data["server"]["protocol"]
# 主机号
HOST: str = config_manager.config_data["server"]["host"]
# 端口号
PORT: int = config_manager.config_data["server"]["port"]
info(f"服务器配置，协议：{PROTOCOL}，主机：{HOST}，端口：{PORT}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """使用异步生命周期管理"""
    # 创建Playwright工厂实例
    playwright_factory = PlaywrightFactory(config_manager.config_data["playwright"]["launch_options"],config_manager.config_data["playwright"]["context_options"])
    # 根据配置创建工作流实例
    if config_manager.config_data["AI"]["startup_type"] == "deepseek":
        # 创建deepseek工作流实例
        ai_task_flows =  await DeepseekFlows.create(config_manager, playwright_factory)
    elif config_manager.config_data["AI"]["startup_type"] == "doubao":
        # 创建豆包工作流实例
        ai_task_flows =  await DoubaoFlows.create(config_manager, playwright_factory)
    elif config_manager.config_data["AI"]["startup_type"] == "skywork":
        # 创建豆包工作流实例
        ai_task_flows =  await SkyworkFlows.create(config_manager, playwright_factory)
    else:
        critical("配置中存在不支持的AI任务类型")
        exit()   # 退出程序
    # 存储在应用程序的状态
    app.state.config_manager = config_manager
    app.state.playwright_factory = playwright_factory
    app.state.ai_task_flows = ai_task_flows
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

"""系统接口"""
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
    df: DoubaoFlows = app.state.ai_task_flows
    await df.home_page.page.screenshot(path=get_root() / "outputs" / "screenshots" / "screenshots.png")
    return FileResponse(path=get_root() / "outputs" / "screenshots" / "screenshots.png")

# websocket实现状态截图传输
@app.websocket("/ws/monitor")
async def ws_monitor(websocket: WebSocket):
    await websocket.accept()
    page = app.state.ai_task_flows.home_page.page

    try:
        while True:
            # 不传 path，直接获取 bytes 对象（内存操作，无磁盘读取）
            screenshot_bytes = await page.screenshot(
                type="jpeg",    # 使用 jpeg 格式降低单帧体积
                quality=60,
                scale="css"  # 缩放模式，可以进一步减小传输体积
            )
            # 发送二进制数据
            await websocket.send_bytes(screenshot_bytes)
            # 30帧/秒(0.01s 约等于 60FPS)，对于监控自动化流程绰绰有余
            await asyncio.sleep(0.03)

    except WebSocketDisconnect:
        info("远程查看连接已断开")
    except Exception as e:
        critical(f"远程状态查看异常: {e}")

@app.get("/status",  response_class=HTMLResponse)
async def status():
    # # 直接从app.state获取对象
    # df: DoubaoFlows = app.state.ai_task_flows
    # try:
    #     # FastAPI 内部调用 requests 访问 9222 端口
    #     response = requests.get("http://127.0.0.1:9222/json", timeout=10)
    # except Exception as e:
    #     return {"error": f"无法连接到浏览器: {str(e)}"}
    html_content = f'''
        <!DOCTYPE html>
        <html>
        <head><title>实时监控</title></head>
        <body>
            <canvas id="display" style="width:100%; height:100vh; display:block; object-fit: contain;"></canvas>
            <script>
                // 获取Canvas和上下文
                const canvas = document.getElementById('display');
                const ctx = canvas.getContext('2d');
                // 建立WebSocket连接
                const ws = new WebSocket(`ws://${{location.host}}/ws/monitor`);
                //const ws = new WebSocket(`{{response.json()[0]["webSocketDebuggerUrl"]}}`);
                // WebSocket 接收的是二进制字节流
                ws.binaryType = "arraybuffer";
                ws.onmessage = async (event) => {{
                    try {{
                        // 将 ArrayBuffer 转为 Blob (JPEG 格式)
                        const blob = new Blob([event.data], {{ type: 'image/jpeg' }});
                        // 使用 createImageBitmap 进行异步解码（不阻塞 UI 线程）
                        const bitmap = await createImageBitmap(blob);
                        // 如果尺寸变化，调整画布
                        if (canvas.width !== bitmap.width) {{
                            canvas.width = bitmap.width;
                            canvas.height = bitmap.height;
                        }}
                        // 绘制并立即释放资源
                        ctx.drawImage(bitmap, 0, 0);
                        bitmap.close(); 
                        
                    }} catch (err) {{
                        console.error("解析帧失败:", err);
                    }}
                }};
                ws.onclose = () => console.log("监控已断开");
                ws.onerror = (e) => console.error("连接错误:", e);
            </script>
        </body>
        </html>
        '''
    # img.src = "{PROTOCOL}://{HOST}:{PORT}/screenshots?t=" + new Date().getTime();
    return HTMLResponse(content=html_content)

"""对话操作"""
# get文本对话
@app.get("/ask/{question}")
async def ask_get(question: str):
    df: DoubaoFlows = app.state.ai_task_flows
    if question == "":
        return {
            "error": "大哥，你输入问题呀"
        }
    # 提问（结果可能是元组或文本）
    result = await df.ask(question)
    # 判断返回结果是否为元组
    if isinstance(result, tuple):
        text_answer, img_urls = result
        return {
            "AI回复": text_answer,
            "图片链接": img_urls
        }
    return {
        "AI回复": result
    }


# post对话
@app.post("/ask")
async def ask_post(ask_model: AskModel):
    # 直接从app.state获取对象
    df: DoubaoFlows = app.state.ai_task_flows
    if ask_model.question == "":
        return {
            "error": "大哥，你输入问题呀"
        }
    try:
        # 提问（问题转成字典并解引用，结果可能是元组或文本）
        result = await df.ask(**ask_model.model_dump())
        # 判断返回结果是否为元组
        if isinstance(result, tuple):
            text_answer, img_urls = result
            return {
                "AI回复": text_answer,
                "图片链接": img_urls
            }
        return {
            "AI回复": result
        }
    except Exception as e:
        return {
            "error": f"{e}"
        }

# 根据下标获得对话内容（目前只能（默认）获取最后一个）
@app.get("/answer")
async def answer(answer_index: int = 0):
    df: DoubaoFlows = app.state.ai_task_flows
    text_answer, img_urls = await df.get_last_answer()
    return {
        "AI回复": text_answer,
        "图片链接": img_urls
    }

# 深度思考
@app.get("/deep_think")
@app.get("/deep_think/{switch}")
async def deep_think(switch: bool = True):
    df: DoubaoFlows = app.state.ai_task_flows
    await df.home_page.deep_thinking_mode(switch)
    if switch:
        return {"info": "已开启深度思考模式"}
    else:
        return {"error": "已关闭深度思考模式"}
# 图片生成模式
@app.get("/image_generation")
@app.get("/image_generation/{switch}")
async def image_generation(switch: bool = True):
    df: DoubaoFlows = app.state.ai_task_flows
    await df.home_page.image_generation_mode(switch)
    if switch:
        return {"info": "已开启图片生成模式"}
    else:
        return {"error": "已关闭图片生成模式"}

# 帮我写作模式
@app.get("/help_me_write")
@app.get("/help_me_write/{switch}")
async def help_me_write(switch: bool = True):
    df: DoubaoFlows = app.state.ai_task_flows
    await df.home_page.help_me_write_mode(switch)
    if switch:
        return {"info": "已开启帮我写作模式"}
    else:
        return {"error": "已关闭帮我写作模式"}

# 视频生成模式
@app.get("/video_generation")
@app.get("/video_generation/{switch}")
async def video_generation(switch: bool = True):
    df: DoubaoFlows = app.state.ai_task_flows
    await df.home_page.video_generation_mode(switch)
    if switch:
        return {"info": "已开启视频生成模式"}
    else:
        return {"error": "已关闭视频生成模式"}

"""会话管理(增删改查)"""
# 创建新会话
@app.post("/conversations")
async def create_conversation():
    df: DoubaoFlows = app.state.ai_task_flows
    return await df.create_conversation()

# 删除会话
@app.delete("/conversations")
@app.delete("/conversations/{identifier}")
async def delete_conversation(identifier: int |str = 0):
    df: DoubaoFlows = app.state.ai_task_flows
    # 判断是否为数字
    if isinstance(identifier, str) and identifier.isdigit():
        identifier = int(identifier)
    # 使用下标删除会话
    if await df.del_conversation(identifier) is False:
        return {"error": f"删除会话失败：找不到下标为 '{identifier}' 的会话"}

    return {"info": f"下标为{identifier}的会话删除成功" if isinstance(identifier, int) else f"标题为{identifier}的对话删除成功"}

# 切换会话
@app.put("/conversations")
@app.put("/conversations/{identifier}")
async def switch_conversation(identifier: int |str = 0):
    df: DoubaoFlows = app.state.ai_task_flows
    # 判断是否为数字
    if isinstance(identifier, str) and identifier.isdigit():
        identifier = int(identifier)
    # 使用下标删除会话
    if await df.switch_conversation(identifier) is False:
        return {"error": f"切换会话失败：找不到下标为 '{identifier}' 的会话"}

    return {"info": f"下标为{identifier}的会话切换成功" if isinstance(identifier, int) else f"标题为{identifier}的对话切换成功"}

# 获得会话标题列表
@app.get("/conversations/title/list")
async def get_conversation_title_list():
    df: DoubaoFlows = app.state.ai_task_flows
    return await df.get_conversation_title_list()

# 获取会话数量
@app.get("/conversations/count")
async def get_conversation_count():
    df: DoubaoFlows = app.state.ai_task_flows
    return await df.get_conversation_count()


if __name__ == "__main__":
    # 2021.03.25是爱丽丝的生日
    uvicorn.run(app, host=HOST, port=PORT)