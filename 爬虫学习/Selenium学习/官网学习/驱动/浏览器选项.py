"""
在 Selenium 3 中, capabilities 是借助"Desired Capabilities"类定义于会话中的.
从 Selenium 4 开始, 您必须使用浏览器选项类.
对于远程驱动程序会话, 浏览器选项实例是必需的, 因为它确定将使用哪个浏览器.
这些选项在 Capabilities 的 w3c 规范中进行了描述.
每个浏览器都有 自定义选项 , 是规范定义之外的内容.
"""
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType

# 测试页面加载策略为'normal'模式
def test_page_load_strategy_normal():
    # 获取默认的Chrome选项配置
    options = get_default_chrome_options()
    # 设置页面加载策略为'normal'（等待所有资源加载完成）
    options.page_load_strategy = 'normal'
    # 创建Chrome浏览器驱动实例
    driver = webdriver.Chrome(options=options)
    # 访问Selenium官网
    driver.get("https://www.selenium.dev/")
    # 退出浏览器
    driver.quit()

# 测试页面加载策略为'eager'模式
def test_page_load_strategy_eager():
    # 获取默认的Chrome选项配置
    options = get_default_chrome_options()
    # 设置页面加载策略为'eager'（DOM加载完成即可，不等待资源）
    options.page_load_strategy = 'eager'
    # 创建Chrome浏览器驱动实例
    driver = webdriver.Chrome(options=options)
    # 访问Selenium官网
    driver.get("https://www.selenium.dev/")
    # 退出浏览器
    driver.quit()

# 测试页面加载策略为'none'模式
def test_page_load_strategy_none():
    # 获取默认的Chrome选项配置
    options = get_default_chrome_options()
    # 设置页面加载策略为'none'（不等待页面加载）
    options.page_load_strategy = 'none'
    # 创建Chrome浏览器驱动实例
    driver = webdriver.Chrome(options=options)
    # 访问Selenium官网
    driver.get("https://www.selenium.dev/")
    # 退出浏览器
    driver.quit()

# 测试脚本执行超时设置
def test_timeouts_script():
    # 获取默认的Chrome选项配置
    options = get_default_chrome_options()
    # 设置脚本执行超时时间为5秒
    options.timeouts = {'script': 5000}
    # 创建Chrome浏览器驱动实例
    driver = webdriver.Chrome(options=options)
    # 访问Selenium官网
    driver.get("https://www.selenium.dev/")
    # 退出浏览器
    driver.quit()

# 测试页面加载超时设置
def test_timeouts_page_load():
    # 获取默认的Chrome选项配置
    options = get_default_chrome_options()
    # 设置页面加载超时时间为5秒
    options.timeouts = {'pageLoad': 5000}
    # 创建Chrome浏览器驱动实例
    driver = webdriver.Chrome(options=options)
    # 访问Selenium官网
    driver.get("https://www.selenium.dev/")
    # 退出浏览器
    driver.quit()

# 测试隐式等待超时设置
def test_timeouts_implicit_wait():
    # 获取默认的Chrome选项配置
    options = get_default_chrome_options()
    # 设置隐式等待超时时间为5秒
    options.timeouts = {'implicit': 5000}
    # 创建Chrome浏览器驱动实例
    driver = webdriver.Chrome(options=options)
    # 访问Selenium官网
    driver.get("https://www.selenium.dev/")
    # 退出浏览器
    driver.quit()

# 测试未处理提示框的行为设置
def test_unhandled_prompt():
    # 获取默认的Chrome选项配置
    options = get_default_chrome_options()
    # 设置未处理提示框的行为为自动接受
    options.unhandled_prompt_behavior = 'accept'
    # 创建Chrome浏览器驱动实例
    driver = webdriver.Chrome(options=options)
    # 访问Selenium官网
    driver.get("https://www.selenium.dev/")
    # 退出浏览器
    driver.quit()

# 测试窗口矩形设置功能（Firefox特有）
def test_set_window_rect():
    # 创建Firefox浏览器选项实例
    options = webdriver.FirefoxOptions()
    # 启用窗口矩形设置功能（Firefox完全支持）
    options.set_window_rect = True  # Full support in Firefox
    # 创建Firefox浏览器驱动实例
    driver = webdriver.Firefox(options=options)
    # 访问Selenium官网
    driver.get("https://www.selenium.dev/")
    # 退出浏览器
    driver.quit()

# 测试严格文件交互性检查
def test_strict_file_interactability():
    # 获取默认的Chrome选项配置
    options = get_default_chrome_options()
    # 启用严格文件交互性检查
    options.strict_file_interactability = True
    # 创建Chrome浏览器驱动实例
    driver = webdriver.Chrome(options=options)
    # 访问Selenium官网
    driver.get("https://www.selenium.dev/")
    # 退出浏览器
    driver.quit()

# 测试代理设置
def test_proxy():
    # 获取默认的Chrome选项配置
    options = get_default_chrome_options()
    # 设置代理配置：手动代理类型，HTTP代理地址和端口
    options.proxy = Proxy({'proxyType': ProxyType.MANUAL, 'httpProxy': 'http.proxy:1234'})
    # 创建Chrome浏览器驱动实例
    driver = webdriver.Chrome(options=options)
    # 访问Selenium官网
    driver.get("https://www.selenium.dev/")
    # 退出浏览器
    driver.quit()

# 测试浏览器名称设置
def test_set_browser_name():
    # 获取默认的Chrome选项配置
    options = get_default_chrome_options()
    # 验证浏览器名称是否为'chrome'
    assert options.capabilities['browserName'] == 'chrome'
    # 创建Chrome浏览器驱动实例
    driver = webdriver.Chrome(options=options)
    # 访问Selenium官网
    driver.get("https://www.selenium.dev/")
    # 退出浏览器
    driver.quit()

# 测试浏览器版本设置
def test_set_browser_version():
    # 获取默认的Chrome选项配置
    options = get_default_chrome_options()
    # 设置浏览器版本为'stable'（稳定版）
    options.browser_version = 'stable'
    # 验证浏览器版本是否已设置为'stable'
    assert options.capabilities['browserVersion'] == 'stable'
    # 创建Chrome浏览器驱动实例
    driver = webdriver.Chrome(options=options)
    # 访问Selenium官网
    driver.get("https://www.selenium.dev/")
    # 退出浏览器
    driver.quit()

# 测试平台名称设置
def test_platform_name():
    # 获取默认的Chrome选项配置
    options = get_default_chrome_options()
    # 设置平台名称为'any'（任意平台）
    options.platform_name = 'any'
    # 创建Chrome浏览器驱动实例
    driver = webdriver.Chrome(options=options)
    # 访问Selenium官网
    driver.get("https://www.selenium.dev/")
    # 退出浏览器
    driver.quit()

# 测试接受不安全证书设置
def test_accept_insecure_certs():
    # 获取默认的Chrome选项配置
    options = get_default_chrome_options()
    # 设置接受不安全的SSL证书
    options.accept_insecure_certs = True
    # 创建Chrome浏览器驱动实例
    driver = webdriver.Chrome(options=options)
    # 访问Selenium官网
    driver.get("https://www.selenium.dev/")
    # 退出浏览器
    driver.quit()

# 获取默认Chrome选项配置的辅助函数
def get_default_chrome_options():
    # 创建Chrome浏览器选项实例
    options = webdriver.ChromeOptions()
    # 添加无沙盒模式参数（常用于Linux环境或容器环境）
    options.add_argument("--no-sandbox")
    # 返回配置好的选项对象
    return options