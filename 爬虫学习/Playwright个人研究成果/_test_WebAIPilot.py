# 自己的模块
import json

from playwright.sync_api import sync_playwright

from utils import logger_manager, info, critical    # 导入日志记录器模块
from utils import ConfigManager # 导入配置管理模块


# 创建配置管理器实例（这是个单例）
config_manager = ConfigManager()
# 层叠覆盖原来的日志配置
config_manager.config_override()    # 层叠覆盖原来的配置
info("日志模块加载完成，全局异常捕获开启")

# print(config_manager.config_data)

print(json.dumps(config_manager.config_data))

playwright = sync_playwright().start()
browser = playwright.chromium.launch()
context = browser.new_context()
page1 = context.new_page()
page2 = context.new_page()
page3 = context.new_page()
page4 = context.new_page()
context.close()
browser.close()
playwright.stop()