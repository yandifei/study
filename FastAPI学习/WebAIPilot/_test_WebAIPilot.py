"""WebAIPilot.py
程序主入口
优先加载日志记录器
"""
# 内置库
import asyncio
import warnings
# 自己的模块
from utils import logger_manager, info, critical    # 导入日志记录器模块
from utils import ConfigManager # 导入配置管理模块
from utils.playwright_factory.playwright_factory import PlaywrightFactory
from logic.deepseek_logic.deepseek_flows import DeepseekFlows
from logic.doubao_logic.doubao_flows import DoubaoFlows

# # 忽略 asyncio 关于未关闭传输的 ResourceWarning（工厂会自动回收资源）
# warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed transport")
# warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed event loop")

# 创建配置管理器实例（这是个单例）
config_manager = ConfigManager(debug=True)
# 层叠覆盖原来的日志配置
config_manager.config_override()    # 层叠覆盖原来的配置
info("日志模块加载完成，全局异常捕获开启")


async def main():
    # 创建Playwright工厂实例
    playwright_factory = PlaywrightFactory(config_manager.config_data["playwright"]["launch_options"],
                                           config_manager.config_data["playwright"]["context_options"])
    # 创建deepseek工作流实例
    df =  await DeepseekFlows.create(config_manager, playwright_factory)
    # # 提问
    text_answer = await df.ask("你好", "data/验证码1.jpg")
    info(f"答案：{text_answer}")
    # text_answer = await df.ask("你能干啥？20字")
    # info(f"答案：{text_answer}")
    # # 获取最后一次的答案
    # info(await df.home_page.get_last_answer())
    # # 获取所有会话
    # info(await df.home_page.get_all_conversation_turn())
    # # 创建会话
    # await df.home_page.create_conversation()
    # # 切换会话
    # await df.home_page.switch_conversation("AI助手热情自我介绍")
    # # 获得所有会话数量
    # info(await df.home_page.get_conversation_count())
    # # 获得所有会话标题
    # titles = await df.home_page.get_conversation_title_list()
    # info(titles)
    # # 删除会话
    # await df.home_page.del_conversation(titles[0])
    # await df.home_page.page.wait_for_timeout(3000000)
    # await df.deep_thinking_mode()
    # await df.network_mode()
    await df.home_page.page.wait_for_timeout(10000)
    # 关闭Playwright工厂实例（手动好看，但也能自动管理的）
    await playwright_factory.close_factory()
    info("Playwright工厂已关闭")

asyncio.run(main())
# app = FastAPI()
# router= APIRouter()
# @router.get("/foo")
# async def foo():
# return "foo"
# @router.get("/bar")
# async def get_item_by_id(item_id:int):
# return "bar"
# app.include_router(router,
# prefix="/items