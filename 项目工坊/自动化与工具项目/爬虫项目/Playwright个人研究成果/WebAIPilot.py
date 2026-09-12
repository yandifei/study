"""WebAIPilot.py
程序主入口
优先加载日志记录器
"""
# 内置库
# 在所有 import 之前，最顶部加入这行（关键！
import nest_asyncio; nest_asyncio.apply()  # 允许嵌套事件循环，解决 Playwright sync + uvicorn 冲突
# from starlette.concurrency import run_in_threadpool   # 没用：Playwright 的同步 API 使用了 greenlet，而 greenlet 不能跨线程切换
import asyncio
from pathlib import Path
# 第三方库
from fastapi import FastAPI # API设计
import uvicorn              # 服务器模块
from pydantic import BaseModel
# 自己的模块
from utils import logger_manager, info, critical    # 导入日志记录器模块
from utils import ConfigManager # 导入配置管理模块
from utils.playwright_factory.playwright_factory import PlaywrightFactory
from logic.doubao_logic.doubao_flows import DoubaoFlows
# 创建配置管理器实例（这是个单例）
config_manager = ConfigManager(debug=True)
# 层叠覆盖原来的日志配置
config_manager.config_override()    # 层叠覆盖原来的配置
info("日志模块加载完成，全局异常捕获开启")

# 创建Playwright工厂实例
playwright_factory = PlaywrightFactory(config_manager.config_data["playwright"]["launch_options"],
    config_manager.config_data["playwright"]["context_options"])
# 创建豆包工作流实例
df = DoubaoFlows(config_manager, playwright_factory)
# # 关闭Playwright工厂实例
# playwright_factory.close()
# 关闭浏览器
df.close_browser()
info("浏览器已关闭")
# 关闭Playwright工厂实例
playwright_factory.close()
info("Playwright工厂已关闭")
#
# # 创建FastAPI实例
# app = FastAPI()
#
#
# @app.get("/")
# def root():
#     return {"服务器状态": "服务器启动成功"}
#
#
# # 问题模型
# class Ask(BaseModel):
#     question: str
#     files: str | Path | list[str | Path] | None = None
#
# @app.post("/ask")
# async def ask_post(ask: Ask):
#     text_answer, img_urls = await asyncio.to_thread(
#         df.home_page.ask,
#         ask.question,
#         ask.files
#     )
#     return {
#         "AI回复": text_answer,
#         "图片链接": img_urls
#     }
#
#
#
#
# if __name__ == "__main__":
#     try:
#         async def main():
#             config = uvicorn.Config(
#                 app,
#                 host="127.0.0.1",
#                 port=8421,
#                 log_level="info"
#             )
#             server = uvicorn.Server(config)
#             await server.serve()
#         # 运行异步主函数
#         asyncio.run(main())
#
#     except KeyboardInterrupt:
#         info("服务器关闭，开始回收资源")
#     finally:
#         # 关闭浏览器
#         df.close_browser()
#         info("浏览器已关闭")
#         # 关闭Playwright工厂实例
#         playwright_factory.close()
#         info("Playwright工厂已关闭")