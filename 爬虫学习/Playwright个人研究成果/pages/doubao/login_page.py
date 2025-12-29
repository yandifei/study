"""login_page.py
豆包登陆界面
"""
# 第三方库
from playwright.sync_api import Page
# 自己的模块
from pages.base_page import BasePage
from utils import ConfigManager, info


class LoginPage(BasePage):
    """豆包登陆界面
    """

    def __init__(self, page, config_manager: ConfigManager):
        """初始化
        :param page:实例化的界面对象
        :param config_manager: 配置
        """
        super().__init__(page)
        # 界面对象
        self.page: Page = page
        # 去到登陆网址
        self.page.goto(config_manager.config_data["AI"]["doubao"]["login_url"])
        # 等待界面加载完成
        self.wait_for_load_state("domcontentloaded")
        # self.page.locator('img[src="https://lf-flow-web-cdn.doubao.com/obj/flow-doubao/samantha/logo-icon-white-bg.png"]').wait_for()


    # def check_login(self):
    #     """检查是否登陆成功
    #     """
    #     # 检查登陆按钮是否可见
    #     if self.page.get_by_test_id("to_login_button").wait_for(timeout=2000, state="visible"):
    #         self.page.get_by_test_id("to_login_button").click()
    #         info("需要手动登陆豆包")
    #         # 直到登陆按钮检测不到才算登陆成功
    #         while not self.page.get_by_test_id("to_login_button").wait_for(timeout=1000, state="visible"):
    #             sleep(1)
    #         info("手动登陆豆包成功")
    #     return True


    def login(self):
        """登陆（用户手动登陆）
        """
        self.page.wait_for_timeout(3000)  # 强制等待 2 秒
        # 检查登陆按钮是否可见
        if self.page.get_by_test_id("to_login_button").is_visible():
            # 点击登陆按钮
            self.page.get_by_test_id("to_login_button").click()
            info("需要用户手动登陆豆包")
            # 等待登陆弹窗出现
            self.page.locator('#dialog-0').wait_for()
            # 直到登陆按钮和登陆界面检测不到才算登陆成功
            while self.page.get_by_test_id("to_login_button").is_visible() or self.page.locator('#dialog-0').is_visible():
                # 等待1秒
                self.page.wait_for_timeout(1000)
        else:
            info("上下文状态注入成功，已完成豆包登陆")
        return True

