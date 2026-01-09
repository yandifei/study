"""login_page.py
豆包登陆界面
"""
# 第三方库
from playwright.async_api import Page
# 自己的模块
from pages.base_page import BasePage
from utils import ConfigManager, info


class LoginPage(BasePage):
    """豆包登陆界面
    """

    async def _async_init(self):  # 实现基类的抽象方法
        """
        异步初始化豆包登陆页面
        :return: None
        """
        # 去到登陆网址
        await self.page.goto(self.cm.config_data["AI"]["doubao"]["login_url"])
        # 等待界面加载完成
        await self.wait_for_load_state("domcontentloaded")
        # self.page.locator('img[src="https://lf-flow-web-cdn.doubao.com/obj/flow-doubao/samantha/logo-icon-white-bg.png"]').wait_for()
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
        # 检查登陆按钮是否可见
        await self.page.wait_for_timeout(3000)  # 强制等待 3 秒
        # 检查登陆按钮是否可见
        if await self.page.get_by_test_id("to_login_button").is_visible():
            info("需要用户手动登陆豆包")
            return False
        info("上下文状态注入成功，已完成豆包登陆")
        return True


    async def login(self):
        """登陆（用户手动登陆）
        """
        await self.page.wait_for_timeout(3000)  # 强制等待 2 秒
        # 检查登陆按钮是否可见
        if await self.page.get_by_test_id("to_login_button").is_visible():
            # # 鼠标悬浮到按钮上
            # self.page.get_by_test_id("to_login_button").hover()
            # 点击登陆按钮
            await self.page.get_by_test_id("to_login_button").click()
            info("请用户手动输入账号和验证码完成豆包登陆")
            # 等待登陆弹窗出现
            await self.page.locator('#dialog-0').wait_for()
            # 直到登陆按钮和登陆界面检测不到才算登陆成功
            while await self.page.get_by_test_id("to_login_button").is_visible() or await self.page.locator('#dialog-0').is_visible():
                # 等待1秒
                await self.page.wait_for_timeout(1000)
        else:
            info("上下文状态注入成功，已完成豆包登陆")
        return True

