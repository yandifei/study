"""doubao_flows.py
豆包工作流
"""
from time import sleep

from pages.doubao.home_page import HomePage
from pages.doubao.login_page import LoginPage
from utils import ConfigManager, info
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
        # 为了拿到回答返回结果，需要hook
        context.add_init_script("""
        // 初始化全局变量
        window.tempCopyBuffer = ""; 
        // 改变js行为
        document.addEventListener('copy', (event) => {
            // 阻止原来的startMonitoring 运行
            event.stopImmediatePropagation();
            // 拦截行为：阻止事件冒泡和默认行为
            event.preventDefault();
            // 同步获取：直接从当前选区抓取文本，存储到变量
            window.tempCopyBuffer = document.getSelection().toString();
        }, true);""")
        # 创建标签页
        page = context.new_page()
        # 创建登录页面
        login_pate = LoginPage(page, config_manager)
        # 检查是否登陆成功
        login_pate.login()
        # 保存登录状态
        context.storage_state(path=self.cm.config_data["playwright"]["context_options"].storage_state)
        # 创建主页面
        home_page = HomePage(page, config_manager)
        # 开个模式
        home_page.deep_thinking_mode()
        # 提问
        text_answer, img_urls = home_page.ask("识别图片中的角色并生成多张相似的", "data/test.png")
        info(f"最终拿到的文本回答: {text_answer}")
        info(f"原图生成链接：{img_urls}")
        # 创建会话
        home_page.create_conversation()
        # 删除会话
        home_page.del_conversation()
        sleep(20)

        self.pf.close_browser(browser)