"""doubao_flows.py
豆包工作流
"""
from pathlib import Path
from typing import Sequence, Coroutine, Any

# 第三方库
from playwright.async_api import Page, FilePayload
# 自己的模块
from pages.doubao.home_page import HomePage
from pages.doubao.login_page import LoginPage
from utils import ConfigManager, info
from utils.playwright_factory.playwright_factory import PlaywrightFactory

class DoubaoFlows:
    """豆包工作流
    """

    @classmethod
    async def create(cls, config_manager: ConfigManager, playwright_factory: PlaywrightFactory):
        """
        标准的异步工厂方法。
        创建、初始化并返回一个完全就绪的页面对象。
        """
        instance = cls(config_manager, playwright_factory)  # 同步构造
        await instance._async_init()  # 仅做页面导航和基本等待，异步初始化
        return instance

    def __init__(self, config_manager: ConfigManager, playwright_factory: PlaywrightFactory):
        self.cm = config_manager
        self.pf = playwright_factory
        self.browser = None
        self.context = None
        self.page: Page | None = None
        self.login_page: LoginPage | None = None
        self.home_page: HomePage | None = None

    async def _async_init(self):
        """内部初始化逻辑"""
        self.browser = await self.pf.new_browser()
        self.context = await self.pf.new_context(self.browser)
        # 注入反爬脚本与 Hook
        await self.context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => false });
            window.tempCopyBuffer = ""; 
            document.addEventListener('copy', (event) => {
                event.stopImmediatePropagation();
                event.preventDefault();
                window.tempCopyBuffer = document.getSelection().toString();
            }, true);
        """)
        # 创建标签页
        self.page = await self.context.new_page()
        # 创建登录页面
        self.login_page = await LoginPage.create(self.page, self.cm)
        # 检查是否登陆成功
        await self.login_page.login()
        # 保存登录状态
        await self.context.storage_state(path=self.cm.config_data["playwright"]["context_options"].storage_state)
        # 创建主页面
        self.home_page = await HomePage.create(self.page, self.cm)


    async def ask(self, question: str, files: str | Path | FilePayload | Sequence[str | Path] | Sequence[FilePayload] | None = None):
        """业务方法示例"""
        # 确保调用的是异步方法
        return await self.home_page.ask(question, files)

    # async def close(self):
    #     """异步关闭浏览器"""
    #     if self.browser:
    #         await self.pf.close_browser(self.browser)
