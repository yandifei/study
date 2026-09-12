# 自己的模块
import json
from pathlib import Path
from time import sleep

from playwright.sync_api import sync_playwright


from utils import logger_manager, info, critical    # 导入日志记录器模块
from utils import ConfigManager # 导入配置管理模块
from utils.playwright_factory.playwright_factory import PlaywrightFactory

# 创建配置管理器实例（这是个单例）
config_manager = ConfigManager()
# 层叠覆盖原来的日志配置
config_manager.config_override()    # 层叠覆盖原来的配置
info("日志模块加载完成，全局异常捕获开启")

# print(config_manager.config_data)

# print(json.dumps(config_manager.config_data))

# playwright = sync_playwright().start()
# browser = playwright.chromium.launch()
# context = browser.new_context()
# page1 = context.new_page()
# page2 = context.new_page()
# page3 = context.new_page()
# page4 = context.new_page()
# context.close()
# browser.close()
# playwright.stop()
#
# pf = PlaywrightFactory(config_manager.config_data["playwright"]["launch_options"],
#     config_manager.config_data["playwright"]["context_options"])
# pf_launch_options = pf.get_launch_options()
# browser = pf.new_browser()
# context = pf.new_context(browser)
# page1 = context.new_page()
# page2 = context.new_page()
# page3 = context.new_page()
# pf.close_browser(browser)




pf = PlaywrightFactory(config_manager.config_data["playwright"]["launch_options"],
    config_manager.config_data["playwright"]["context_options"])
pf_launch_options = pf.get_launch_options()
# print(pf_launch_options)
browser = pf.new_browser()
context = pf.new_context(browser)
page = context.new_page()
# 基础伪装：清除 webdriver 标志
page.add_init_script("""Object.defineProperty(navigator, 'webdriver', { get: () => false });""")
page.goto("https://www.baidu.com")
page.screenshot(path=Path(config_manager.config_data["playwright"]["screen_dir"], "baidu.png"))
sleep(10)
pf.close_context(context)
pf.close_browser(browser)
# 有没有close都无所谓，因为它会自动处理
pf.close()
