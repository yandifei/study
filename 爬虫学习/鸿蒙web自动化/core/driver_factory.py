"""driver_factory.py
驱动器工厂（Driver Factory），表明其职责是创建和生产配置好的 WebDriver 实例
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class DriverFactory:
    def __init__(self, chromedriver_path: str = r"chromedriver.exe",
                 chrome_path: str = r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                 headless_chrome_path: str = r"Google Chrome Headless\chrome-headless-shell.exe"):
        r"""
        web自动化的基础配置进行封装，处理驱动驱动创建，也就是生产不同的浏览器驱动
        :param chromedriver_path: 谷歌驱动路径，默认当前目录下
        :param chrome_path: 谷歌浏览器位置，默认系统的C:\Program Files\Google\Chrome\Application
        :param headless_chrome_path: 无头谷歌浏览器位置，默认当前目录下的的Google Chrome Headless\chrome-headless-shell.exe
        """
        # 创建Chrome浏览器选项实例
        self.options = webdriver.ChromeOptions()
        # --------------------- 性能和稳定性优化参数 ---------------------
        # 禁用或减少浏览器内部的日志输出。减轻文件 I/O 负担。
        self.options.add_argument("--disable-logging")
        # 确保静音，减少资源占用。
        self.options.add_argument("--mute-audio")
        # --------------------- 资源节约和后台任务禁用 ---------------------
        # 禁用扩展（扩展会增加资源消耗）
        self.options.add_argument("--disable-extensions")
        # 禁用 Chrome 的默认应用程序
        self.options.add_argument("--disable-default-apps")
        # 阻止浏览器进行任何后台网络活动
        self.options.add_argument("--disable-background-networking")
        # 禁用 Chrome 的同步功能
        self.options.add_argument("--disable-sync")
        # 禁用域名可靠性监测
        self.options.add_argument("--disable-domain-reliability")
        # 跳过首次运行向导
        self.options.add_argument("--no-first-run")
        # --------------------- 启动和兼容性优化（尤其针对 Linux/容器） ---------------------
        # 禁用沙盒模式（常用于 Linux 环境或容器环境）
        self.options.add_argument("--no-sandbox")
        # 禁用 setuid 沙盒（用于解决 Linux 权限问题）
        self.options.add_argument("--disable-setuid-sandbox")
        # 禁用 /dev/shm 共享内存（优化 Linux/Windows 内部内存使用）
        self.options.add_argument("--disable-dev-shm-usage")
        # 禁用弹出窗口阻止程序（提高稳定性）
        self.options.add_argument("--disable-popup-blocking")
        # 禁用顶部的“受自动化软件控制”信息条
        self.options.add_argument("--disable-infobars")
        # --------------------- 实验性选项（Experimental Options） ---------------------
        # 禁用自动化检测提示，防止网站检测到 Selenium
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 禁用或隐藏一些 Chrome 浏览器自带的弹出功能，以防止它们干扰测试流程。
        # 偏好设置
        self.prefs = {
            'profile.default_content_setting_values': {  # 控制网站的通知权限
                'notifications': 2  # 隐藏chromedriver的通知
            },
            'credentials_enable_service': False,  # 禁用 Chrome 自动保存密码或提示保存密码的功能（凭证管理服务）
            'profile.password_manager_enabled': False  # 控制 Chrome 是否启用内置的密码管理器（进一步确保 禁用与密码相关的弹出窗口或功能）
        }
        self.options.add_experimental_option('prefs', self.prefs)  # 启用偏好设置
        # 禁用 GPU 硬件加速，规避一些与图形处理相关的已知 Bug 或兼容性问题，尤其是在无头模式（无界面）
        self.options.add_argument('--disable-gpu')
        # 禁用了 CPU 上的备用渲染方案
        self.options.add_argument('--disable-software-rasterizer')
        # 创建服务对象（传入谷歌webdriver驱动路径）
        self.service = Service(executable_path=fr"{chromedriver_path}")
        # 谷歌浏览器位置
        self.chrome_path = fr"{chrome_path}"
        # 无头谷歌浏览器的位置
        self.headless_chrome_path = fr"{headless_chrome_path}"

    def create_driver(self, background: bool):
        """
        创建驱动器，高级创建
        :param background:是否后台
        :return: 驱动器对象
        """
        if background:
            # 无头谷歌浏览器位置
            self.options.binary_location = self.headless_chrome_path
            self.remove_gpu()  # 移除gpu
            driver = webdriver.Chrome(self.options, self.service)
            driver.set_window_size(1920, 1080)  # 固定大小无头窗口防止遮罩
            # 返回驱动对象
            return driver
        else:
            # 默认谷歌浏览器位置
            self.options.binary_location = self.chrome_path
            # 使用默认的浏览器选项和服务创建驱动器
            driver = webdriver.Chrome(self.options, self.service)
            return driver

    def remove_gpu(self):
        # 禁用 GPU 硬件加速，规避一些与图形处理相关的已知 Bug 或兼容性问题，尤其是在无头模式（无界面）
        self.options.add_argument('--disable-gpu')

    def remove_cpu_rendering(self):
        # 禁用了 CPU 上的备用CPU渲染方案
        self.options.add_argument('--disable-software-rasterizer')

    def silent(self) -> bool:
        """
        开启静音参数
        :return: True
        """
        # 静音处理
        self.options.add_argument("--mute-audio")
        return True

    def running_in_the_background(self) -> bool:
        """在后台运行（无头模式）
        :return: True
        """
        # 添加无头模式，不渲染图形界面
        self.options.add_argument("--headless=new")
        # # 添加大小（无头可能很小）
        # self.options.add_argument("--window-size=1920,1080")
        return True

    def remove_image(self) -> bool:
        """
        移除图片资源加载
        :return:True
        """
        self.prefs["profile.managed_default_content_settings.images"] = 2
        return True

    def remove_css(self) -> bool:
        """
        移除css样式加载(移除后可能导致网页结构错乱)
        :return: True
        """
        self.prefs["profile.managed_default_content_settings.stylesheet"] = 2
        return True

    def remove_font(self) -> bool:
        """
        移除字体样式加载
        :return: True
        """
        self.prefs["profile.managed_default_content_settings.fonts"] = 2
        return True

if __name__ == '__main__':
    # df = DriverFactory()
    df = DriverFactory("./Google Chrome/chrome.exe",
                       "./Google Chrome Headless/chrome-headless-shell.exe"
                       )
    print(df.chrome_path)
    print(df.headless_chrome_path)