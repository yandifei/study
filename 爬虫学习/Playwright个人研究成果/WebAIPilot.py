"""WebAIPilot.py
程序主入口
优先加载日志记录器
"""
# 自己的模块
from utils import logger_manager, info, critical    # 导入日志记录器模块
from utils import ConfigManager # 导入配置管理模块


# 创建配置管理器实例（这是个单例）
config_manager = ConfigManager()
# 层叠覆盖原来的日志配置
config_manager.config_override()    # 层叠覆盖原来的配置
info("日志模块加载完成，全局异常捕获开启")

# 开始执行主业务逻辑
from playwright.sync_api import sync_playwright
playwright = sync_playwright().start()

# 关键步骤：使用 'args' 选项传递启动参数
browser = playwright.chromium.launch(
    headless=False,
    args=[
        '--disable-blink-features=AutomationControlled',
    ]
)
context = browser.new_context(
    # 伪造 User-Agent，确保与目标浏览器版本一致
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
    locale="zh-CN",
    timezone_id="Asia/Shanghai"
)

context.set_default_timeout(30000)  # 设置缺省等待时间为30000毫秒

page = context.new_page()

# 1. 基础伪装：清除 webdriver 标志
page.add_init_script("""
Object.defineProperty(navigator, 'webdriver', { get: () => false });
""")


page.goto("https://www.doubao.com/chat/")



# # 等待输入框加载完成
# page.get_by_placeholder("发消息或输入 / 选择技能").wait_for()
# # 输入内容
# page.get_by_placeholder("发消息或输入 / 选择技能").fill("识别图片中的角色")
# page.wait_for_timeout(3000)
# # 点击按钮会触发 file chooser
# with page.expect_file_chooser() as fc_info:
#     # 定位文件输入框
#     page.get_by_test_id("upload_file_button").click()
#
# # 文件选择
# file_chooser = fc_info.value
# page.wait_for_timeout(3000)
#
# # 上传单个文件
# file_chooser.set_files("./data/test.png")
# page.wait_for_timeout(3000)
#
# # 等待文件上传完毕
# page.get_by_test_id("chat_input_send_button").is_enabled()
#
# page.wait_for_timeout(3000)
#
# # 点击发送
# page.get_by_test_id("chat_input_send_button").click()



page.wait_for_timeout(1000000)
browser.close()

playwright.stop()

info("Playwright 关闭完成")