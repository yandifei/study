"""WebAIPilot.py
程序主入口
优先加载日志记录器
"""
from pathlib import Path
from time import sleep

from logic.doubao_logic.doubao_flows import DoubaoFlows
# 自己的模块
from utils import logger_manager, info, critical    # 导入日志记录器模块
from utils import ConfigManager # 导入配置管理模块
from utils.playwright_factory.playwright_factory import PlaywrightFactory

# 创建配置管理器实例（这是个单例）
config_manager = ConfigManager()
# 层叠覆盖原来的日志配置
config_manager.config_override()    # 层叠覆盖原来的配置
info("日志模块加载完成，全局异常捕获开启")

playwright_factory = PlaywrightFactory(config_manager.config_data["playwright"]["launch_options"],
    config_manager.config_data["playwright"]["context_options"])
DoubaoFlows(config_manager, playwright_factory)
playwright_factory.close()


# pf = PlaywrightFactory(config_manager.config_data["playwright"]["launch_options"],
#     config_manager.config_data["playwright"]["context_options"])
# pf_launch_options = pf.get_launch_options()
# # print(pf_launch_options)
# browser = pf.new_browser()
# context = pf.new_context(browser)
# page = context.new_page()
# # 基础伪装：清除 webdriver 标志
# page.add_init_script("""Object.defineProperty(navigator, 'webdriver', { get: () => false });""")
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
# # 关闭所有浏览器
# pf.close_browser(browser)

