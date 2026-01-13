"""skywork_flows.py
天工工作流
"""
from pathlib import Path
from typing import Sequence

# 第三方库
from playwright.async_api import Page, FilePayload
# 自己的模块
from pages.skywork.home_page import HomePage
from pages.skywork.login_page import LoginPage
from utils import ConfigManager, info
from utils.playwright_factory.playwright_factory import PlaywrightFactory

class SkyworkFlows:
    """天工工作流
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
        # 进行登陆操作

        await self.login()
        self.browser = await self.pf.new_browser()
        self.context = await self.pf.new_context(self.browser)
        # 注入反爬脚本与 Hook
        await self.context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => false });
            window.tempCopyBuffer = "";
            navigator.clipboard.writeText = async (text) => {
                window.tempCopyBuffer = text; 
                return Promise.resolve(); // 禁止二次触发
            };
        """)
        # 创建标签页
        self.page = await self.context.new_page()
        # 保存登录状态
        await self.context.storage_state(path=self.cm.config_data["playwright"]["context_options"].storage_state)
        # 创建主页面
        self.home_page = await HomePage.create(self.page, self.cm)

    """登陆流程"""
    async def login(self):
        """登陆流程"""
        # 保存原来的headless配置
        headless = self.cm.config_data["playwright"]["launch_options"].headless
        # 修改配置为有头标志
        self.cm.config_data["playwright"]["launch_options"].headless = False
        # 创建浏览器
        self.browser = await self.pf.new_browser()
        # 创建浏览器上下文
        self.context = await self.pf.new_context(self.browser)
        # 创建标签页
        self.page = await self.context.new_page()
        # # 中途进入全屏模式（最大化要改args参数，如果原来有--start-maximized就不好处理了）
        # await self.page.keyboard.press("F11")
        # 创建登录页面
        self.login_page = await LoginPage.create(self.page, self.cm)
        # 进行登陆操作
        await self.login_page.login()
        # 保存登录状态
        await self.context.storage_state(path=self.cm.config_data["playwright"]["context_options"].storage_state)
        # 关闭当前有头浏览器的会话
        await self.pf.close_context(self.context)
        # 关闭当前有头浏览器
        await self.pf.close_browser(self.browser)
        # 修改配置为原来配置文件中的配置
        self.cm.config_data["playwright"]["launch_options"].headless = headless

    """对话操作"""
    async def ask(self, question: str, files: str | Path | FilePayload | Sequence[str | Path] | Sequence[FilePayload] | None = None):
        """业务方法示例"""
        # 确保调用的是异步方法
        return await self.home_page.ask(question, files)

    async def get_last_answer(self):
        """
        获取最后对话中豆包回复的内容（异步版本）

        :return: 元组 (text_answer: str, img_urls: list[str]) - 返回文本回答和图片URL列表
        """
        return await self.home_page.get_last_answer()

    async def get_all_conversation_turn (self):
        """
        获取所有对话历史（异步版本）

        :return: 所有对话历史的控件
        """
        return self.home_page.get_all_conversation_turn()

    """会话管理(增删改查)"""
    async def create_conversation(self):
        """创建会话"""
        return await self.home_page.create_conversation()

    async def del_conversation(self, identifier: int | str = 0):
        """删除会话（异步版本）"""
        return await self.home_page.del_conversation(identifier)

    async def switch_conversation(self, identifier: int | str = 0):
        """切换会话（异步版本）

        :param identifier: 会话索引，可以是下标、会话的标题
        :return: 成功切换返回True，否则返回False
        """
        return await self.home_page.switch_conversation(identifier)

    async def get_conversation_title_list(self):
        """获取会话列表"""
        return await self.home_page.get_conversation_title_list()

    async def get_conversation_count(self):
        """获取会话列表数量"""
        return await self.home_page.get_conversation_count()

    """对话模式"""
    async def deep_thinking_mode(self, switch: bool = True):
        """切换对话模式"""
        return await self.home_page.deep_thinking_mode(switch)

    async def network_mode(self, switch: bool = True):
        """切换网络模式"""
        return await self.home_page.network_mode(switch)