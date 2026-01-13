"""skywork.py
天工登陆界面
"""
# 第三方库
from playwright.async_api import Page
from playwright.async_api import TimeoutError
# 自己的模块
from pages.base_page import BasePage
from utils import ConfigManager, info


class LoginPage(BasePage):
    """天工登陆界面
    """

    async def _async_init(self):  # 实现基类的抽象方法
        """
        异步初始化天工登陆页面
        :return: None
        """
        # 去到登陆网址
        await self.page.goto(self.cm.config_data["AI"]["skywork"]["login_url"])
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
        # 检测是否已经登陆
        try:
            # 判断是否存在成功登陆的标志位
            await self.page.locator('[class="relative block"]').wait_for(timeout=5000)
        except TimeoutError:
            info("需要用户手动登陆天工")
            return False
        info("上下文状态注入成功，已完成天工登陆")
        return True

    async def login(self):
        """登陆（用户手动登陆）
        """
        # 检测是否已经登陆
        try:
            # 判断是否存在成功登陆的标志位
            await self.page.locator('[class="relative block"]').wait_for(timeout=1000)
            info("上下文状态注入成功，已完成天工登陆")
        except TimeoutError:
            # 点击登陆按钮
            await self.page.locator('.login-btn.cursor-pointer').click(force=True)
            info("需要用户手动登陆天工")
            # 等待登陆界面消失(登陆成功后url不会变)
            while await self.page.locator('.el-overlay.loginModal').is_visible() \
                    or await self.page.locator('.login-btn.cursor-pointer').is_visible():
                await self.page.wait_for_timeout(1000)
            info("上下文状态注入成功，已完成天工登陆")
        return True

