"""WebAIPilot.py
程序主入口
优先加载日志记录器
"""
# 内置库
import asyncio
# from pathlib import Path
# # 第三方库
# from fastapi import FastAPI # API设计
# import uvicorn              # 服务器模块
# from pydantic import BaseModel
# from watchfiles import awatch

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


async def main():
    # 创建Playwright工厂实例
    playwright_factory = PlaywrightFactory(config_manager.config_data["playwright"]["launch_options"],
                                           config_manager.config_data["playwright"]["context_options"])
    # 创建豆包工作流实例
    df =  await DoubaoFlows.create(config_manager, playwright_factory)
    # # 提问
    # text_answer, img_urls = home_page.ask("识别图片中的角色并生成多张相似的", "data/test.png")
    # info(f"最终拿到的文本回答: {text_answer}")
    # info(f"原图生成链接：{img_urls}")
    # # 创建会话
    # home_page.create_conversation()
    # # 删除会话
    # home_page.del_conversation()
    # sleep(20)


    # 关闭工作流实例
    await df.close()
    # 关闭Playwright工厂实例
    playwright_factory.close()
    info("Playwright工厂已关闭")


# main()
asyncio.run(main())
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