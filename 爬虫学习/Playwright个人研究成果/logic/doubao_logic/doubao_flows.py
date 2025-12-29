"""doubao_flows.py
豆包工作流
"""
from pathlib import Path
from time import sleep

from pages.doubao.home_page import HomePage
from pages.doubao.login_page import LoginPage
from utils import ConfigManager
from utils.playwright_factory.playwright_factory import PlaywrightFactory

class DoubaoFlows:
    """豆包工作流
    """
    def __init__(self, config_manager: ConfigManager, playwright_factory: PlaywrightFactory):
        self.cm: ConfigManager = config_manager
        self.pf = playwright_factory
        browser = self.pf.new_browser()
        context = self.pf.new_context(browser)
        # 基础伪装：清除 webdriver 标志
        context.add_init_script("""Object.defineProperty(navigator, 'webdriver', { get: () => false });""")
        # 创建标签页
        page = context.new_page()
        # 创建登录页面
        self.login_pate = LoginPage(page, config_manager)
        # 检查是否登陆成功
        self.login_pate.login()
        # 保存登录状态
        context.storage_state(path=self.cm.config_data["playwright"]["context_options"].storage_state)
        # 创建主页面
        self.home_page = HomePage(page, config_manager)
        # self.home_page.ask("识别图片中的角色并生成一张另一张相似的图片", "data/test.png")
        self.home_page.ask("识别图片中的角色", "data/test.png")
        self.home_page.get_answer()
        sleep(20)

        # # 访问豆包网页
        # page.goto(config_manager.config_data["AI"]["doubao"]["chat_url"])
        # # 等待输入框加载完成
        # page.get_by_placeholder("发消息或输入 / 选择技能").wait_for()
        # # 输入内容
        # page.get_by_placeholder("发消息或输入 / 选择技能").fill("识别图片中的角色")
        # page.wait_for_timeout(3000)
        # # 点击按钮会触发 file chooser
        # with page.expect_file_chooser() as fc_info:
        #     # 定位文件输入框
        #     page.get_by_test_id("upload_file_button").click()
        #     # 文件选择
        #     file_chooser = fc_info.value
        #     page.wait_for_timeout(3000)
        #     # 上传单个文件
        #     file_chooser.set_files("./data/test.png")
        #     page.wait_for_timeout(3000)
        #     # 等待文件上传完毕
        #     page.get_by_test_id("chat_input_send_button").is_enabled()
        #     page.wait_for_timeout(3000)
        # # 点击发送
        # page.get_by_test_id("chat_input_send_button").click()
        # # 截图
        # page.screenshot(path=Path(config_manager.config_data["playwright"]["screen_dir"], "baidu.png"))
        # sleep(10)
        # 关闭所有浏览器
        self.pf.close_browser(browser)