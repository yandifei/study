"""deepseek_flows.py
深度求索工作流
"""
from pathlib import Path
from typing import Sequence

# 第三方库
from playwright.async_api import Page, FilePayload
# 自己的模块
from pages.deepseek.home_page import HomePage
from pages.deepseek.login_page import LoginPage
from utils import ConfigManager, info
from utils.playwright_factory.playwright_factory import PlaywrightFactory

class DeepseekFlows:
    """深度求索工作流
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

    # async def close(self):
    #     """异步关闭浏览器"""
    #     if self.browser:
    #         await self.pf.close_browser(self.browser)

"""
# 注入拦截脚本
const originalWrite = navigator.clipboard.writeText;
navigator.clipboard.writeText = async function(text) {
    console.log('--- 拦截到复制内容 ---');
    console.log('内容长度:', text.length);
    console.log('内容预览:', text.substring(0, 100));
    
    // 关键：打印调用堆栈，找到是谁调用了复制
    console.trace(); 
    
    return originalWrite.call(navigator.clipboard, text);
};


navigator.clipboard.writeText = async (text) => {
    // A. 截获内容到你的变量
    window.tempCopyBuffer = text; 
    console.log("【拦截成功】内容已存入 window.tempCopyBuffer，但不会进入系统剪贴板");

    // B. 关键点：不调用 originalWrite(text)
    // 而是返回一个成功的 Promise，让网页误以为写入剪贴板成功了
    return Promise.resolve(); 
};
"""