"""login_page.py
deepseek登陆界面
"""
# 第三方库
from playwright.async_api import Page
# 自己的模块
from pages.base_page import BasePage
from utils import ConfigManager, info


class LoginPage(BasePage):
    """deepseek登陆界面
    """

    async def _async_init(self):  # 实现基类的抽象方法
        """
        异步初始化deepseek登陆页面
        :return: None
        """
        # 去到登陆网址
        await self.page.goto(self.cm.config_data["AI"]["deepseek"]["login_url"])
        # await self.page.goto(self.cm.config_data["AI"]["deepseek"]["login_url"], wait_until = "networkidle")  # 处理重定向问题
        # 更新初始化状态
        self._is_initialized = True

    def __init__(self, page: Page, config_manager: ConfigManager):
        """初始化
        :param page:实例化的界面对象
        :param config_manager: 配置
        """
        super().__init__(page)
        # 界面对象
        self.page: Page = page
        # 配置
        self.cm: ConfigManager = config_manager


    async def check_login(self):
        """检查是否已登陆成功
        检测到已经登陆返回ture，否则返回false
        """
        # 检测是否已经为登陆的网址
        if self.page.url == self.cm.config_data["AI"]["deepseek"]["chat_url"]:
            info("需要用户手动登陆deepseek")
            return False
        info("上下文状态注入成功，已完成deepseek登陆")
        return True

    async def login(self):
        """登陆（用户手动登陆）
        """
        # 判断是否登陆成功，如果登陆成功会重定向到https://chat.deepseek.com
        if self.page.url == self.cm.config_data["AI"]["deepseek"]["chat_url"]:
            info("上下文状态注入成功，已完成deepseek登陆")
        else:
            info("请用户手动输入账号和验证码完成deepseek登陆")
            # 等待登陆界面消失
            while self.page.url == self.cm.config_data["AI"]["deepseek"]["login_url"]:
                await self.page.wait_for_timeout(1000)
            info("上下文状态注入成功，已完成deepseek登陆")
        return True

