"""playwright_factory.py
设计原则
1.单例 Factory：同一时刻只允许存在一个活跃的 PlaywrightFactory 实例（并发安全）；调用 close() 后会释放单例（_instance=None）
2.显式关闭优先：提供 close() 作为统一的幂等回收入口；业务代码应显式调用 close()（必要时可封装 with 管理，但当前实现未内置 with）。
3.退出兜底：在 Factory 初始化时注册 atexit.register(self.close)，在解释器正常退出时自动触发 close() 做兜底回收（不依赖 __del__）。
4.Browser 复用由调用方决定，Factory 保留多策略扩展能力：Factory 提供 new_browser() 创建并登记多个 Browser；同时提供 get_browser_() 返回已登记 Browser 的副本列表，调用方可自行选择复用哪一个 Browser。后续可扩展“默认复用单 Browser / 按 launch 策略复用”的策略方法，但当前默认不自动复用。
5.所有权（ownership）严格：Factory 仅管理并回收由自己创建并登记的 Browser/Context。new_context(browser=...) 要求传入的 browser 必须来自本 Factory（已登记），否则抛出异常；不支持对外部 browser/context 的隐式接管（后续若需要可新增显式 adopt_* 接口）。
6回收顺序固定且 stop 至多一次：统一回收顺序为 Contexts → Browsers → Playwright。通过 _playwright_flag 保证 close() 幂等：一旦关闭完成，后续再调用 close() 不会重复 stop。
7注册表线程安全，关闭在锁外执行：所有创建/登记/移除（Browser/Context registry）操作均在同一把可重入锁保护下完成；close() 在锁内完成“置状态 + 拷贝 + 清空 registry”，随后在锁外执行实际 close()/stop()，避免阻塞其他线程。
8.Page 不纳入生命周期管理：Factory 仅提供 new_page(context) 的便捷创建，不追踪 Page；Page 的回收依赖 context.close() 的级联行为，如需 Page 级别的特殊回收策略由上层业务实现。
"""
# 内置库
import threading
import atexit
from contextlib import contextmanager
from typing import Literal

# 内置库
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from launch_options import LaunchOptions
# 自己的模块
from context_options import ContextOptions
from utils import debug


class PlaywrightFactory:
    """
    Playwright工厂

    管理sync_playwright()的生命周期，生产browser和context。
    采用单例模式确保全局只有一个Playwright实例。

    注意事项：
    1. 实例化PlaywrightFactory后，LaunchOptions和context_options修改需要通过
       set_launch_options和set_context_options来实现
    2. 使用atexit确保进程退出时自动清理资源
    3. 线程安全的单例模式实现，支持多线程环境

    生命周期管理：
    1. 创建Factory时自动启动Playwright
    2. 可以手动关闭Factory释放所有资源
    3. 支持单个资源的创建和销毁

    使用示例：
        factory = PlaywrightFactory()
        browser = factory.new_browser()
        context = factory.new_context(browser)
        page = factory.new_page(context)
    """

    # 存储单例实例的类变量
    _instance = None

    # 类级锁，确保多线程环境下的线程安全
    _lock = threading.RLock()  # 用可重入锁，避免嵌套调用死锁

    # atexit 只注册一次，且不捕获实例（避免强引用导致多次 create/close 时对象无法释放）
    _atexit_registered = False

    @classmethod
    def _atexit_close(cls) -> None:
        """
        进程退出兜底处理：只关闭当前仍然存活的单例（若存在）。

        注意事项：
        - 不能捕获实例引用，否则会导致旧实例被 atexit 强引用住
        - 退出阶段尽量不抛异常，避免影响正常退出流程

        :raises: 不会主动抛出异常，但会记录调试信息
        """
        inst = cls._instance
        if inst is not None:
            try:
                inst.close()
            except Exception:
                # 退出阶段尽量不抛异常
                pass

    def __new__(cls, launch_options: LaunchOptions | None = None,
                context_options: ContextOptions | None = None) -> 'PlaywrightFactory':
        """
        创建单例实例：线程安全双重检查锁定 (DCL) 实现。

        实现原理：
        1. 首先检查实例是否存在，避免不必要的锁竞争
        2. 如果实例不存在，获取锁确保线程安全
        3. 再次检查实例是否存在，避免在等待锁的过程中实例已被创建
        4. 创建并返回单例实例

        :param launch_options: 浏览器启动配置选项
        :param context_options: 浏览器上下文配置选项
        :return: PlaywrightFactory 单例实例
        """
        # 如果实例已经存在，直接返回
        if cls._instance is None:
            # 获取锁，确保只有一个线程进行实例化
            with cls._lock:
                # 避免在等待锁的过程中，实例已经被其他线程创建
                if cls._instance is None:
                    # 进行实例化操作
                    cls._instance = super().__new__(cls)
        # 返回单例
        return cls._instance

    def __init__(self, launch_options: LaunchOptions | None = None,
                 context_options: ContextOptions | None = None) -> None:
        """
        初始化PlaywrightFactory单例。

        注意事项：
        - 使用`_initialized`标志确保配置只加载一次
        - 自动启动Playwright引擎
        - 注册atexit退出处理器

        :param launch_options: 浏览器启动配置，如果为None则使用默认配置
        :param context_options: 浏览器上下文配置，如果为None则使用默认配置
        """
        with self._lock:
            # 确保配置只加载一次(Pythonic写法)
            if getattr(self, "_initialized", False):
                return
            # 设置被初始化的标志位
            self._initialized = True
            # 启动配置
            self.__launch_options = launch_options if launch_options is not None else LaunchOptions()
            # 上下文配置
            self.__context_options = context_options if context_options is not None else ContextOptions()
            # 创建单一实例的时候就启动playwright，确保它只启动一次
            self.playwright = sync_playwright().start()
            # playwright存在的标志位
            self._playwright_flag = True

            # Registry：只登记自己创建的资源
            self._browser_list: list[Browser] = []
            self._context_list: list[BrowserContext] = []

            # 退出兜底（不依赖 __del__）：类级只注册一次，避免 atexit 强引用旧实例
            if not PlaywrightFactory._atexit_registered:
                atexit.register(PlaywrightFactory._atexit_close)
                PlaywrightFactory._atexit_registered = True

    def get_launch_options(self) -> LaunchOptions:
        """
        安全获取启动配置。

        线程安全地获取当前生效的LaunchOptions实例。

        :return: LaunchOptions的实例，包含当前浏览器启动配置
        """
        with self._lock:
            return self.__launch_options

    def get_context_options(self) -> ContextOptions:
        """
        安全获取上下文配置。

        线程安全地获取当前生效的ContextOptions实例。

        :return: ContextOptions的实例，包含当前浏览器上下文配置
        """
        with self._lock:
            return self.__context_options

    def set_launch_options(self, launch_options: LaunchOptions | None = None) -> LaunchOptions:
        """
        线程安全地更新 Playwright 启动配置（LaunchOptions）。

        说明：
        - 配置更新过程受类级锁保护，保证在多线程环境下的原子性与一致性
        - 仅影响后续使用该Factory创建的browser，不会影响已经创建的browser实例
        - 会记录更新日志

        :param launch_options: 新的启动配置对象，None表示使用默认配置
        :return: 当前生效的LaunchOptions实例
        """
        with self._lock:
            self.__launch_options = launch_options if launch_options is not None else LaunchOptions()
            debug(f"启动配置已更新为：{self.__launch_options.to_dict()}")
        return self.__launch_options

    def set_context_options(self, context_options: ContextOptions | None = None) -> ContextOptions:
        """
        线程安全地更新 Playwright 上下文配置（ContextOptions）。

        说明：
        - 配置更新操作在类级锁保护下执行，避免多线程并发写入导致的状态不一致
        - 更新后的配置仅会作用于后续新创建的context，不会影响已经存在的context实例
        - 会记录更新日志

        :param context_options: 新的上下文配置对象，None表示使用默认配置
        :return: 当前生效的ContextOptions实例
        """
        with self._lock:
            self.__context_options = (
                context_options if context_options is not None else ContextOptions()
            )
            debug(f"上下文配置已更新为：{self.__context_options.to_dict()}")
        return self.__context_options

    def new_browser(self, launch_options: LaunchOptions | None = None,
                    browser_type: Literal["chromium", "firefox", "webkit"] = "chromium") -> Browser:
        """
        安全的创建并登记 Browser

        创建一个新的浏览器实例并将其登记到工厂的管理列表中。

        :param launch_options: 浏览器启动选项，如果不提供则使用工厂默认配置
        :param browser_type: 浏览器类型，支持 "chromium"、"firefox"、"webkit"，默认为 "chromium"
        :return: 创建的 Browser 实例
        :raises RuntimeError: 当 PlaywrightFactory 已关闭时抛出
        :raises ValueError: 当提供了不支持的浏览器类型时抛出
        """
        with self._lock:
            if not self._playwright_flag:
                raise RuntimeError("PlaywrightFactory已关闭，无法创建新资源")
            # 转换 launch_options
            launch_options = (
                launch_options.to_dict() if launch_options is not None else self.__launch_options.to_dict())
            # 判断需要创建的浏览器类型
            if browser_type == "chromium":
                browser = self.playwright.chromium.launch(**launch_options)
            elif browser_type == "firefox":
                browser = self.playwright.firefox.launch(**launch_options)
            elif browser_type == "webkit":
                browser = self.playwright.webkit.launch(**launch_options)
            else:
                raise ValueError(f"不支持的浏览器类型: {browser_type}。支持的类型包括: chromium, firefox, webkit")
            # 将浏览器的实例添加到浏览器列表中进行管理
            self._browser_list.append(browser)
            return browser

    def get_browser_(self) -> list[Browser]:
        """
        安全获得浏览器列表，方便复用

        返回浏览器实例的副本，避免直接操作内部列表。

        :return: 当前工厂管理的浏览器实例列表的副本
        :raises RuntimeError: 当 PlaywrightFactory 已关闭时抛出
        """
        with self._lock:
            if not self._playwright_flag:
                raise RuntimeError("PlaywrightFactory已关闭")
            return self._browser_list.copy()

    def new_context(self, browser: Browser, context_options: ContextOptions | None = None) -> BrowserContext:
        """
        安全的创建并登记 context。

        在指定的浏览器实例中创建一个新的上下文，并将其登记到工厂的管理列表中。

        :param browser: 已登记的浏览器实例，必须是通过本工厂创建的
        :param context_options: 上下文配置，若为 None，使用当前 PlaywrightFactory 的默认配置
        :return: 新创建的 BrowserContext 实例
        :raises RuntimeError: 当 PlaywrightFactory 已关闭时抛出
        :raises ValueError: 当浏览器实例不是通过本工厂创建时抛出
        """
        with self._lock:
            if not self._playwright_flag:
                raise RuntimeError("PlaywrightFactory 已关闭，无法创建新资源")
            # 检查浏览器实例是否是已经注册的
            if browser not in self._browser_list:
                raise ValueError("浏览器实例不是PlaywrightFactory生产的，没有被注册")

            # 转换 context_options
            context_options = (
                context_options.to_dict() if context_options is not None else self.__context_options.to_dict())
            # 创建 context
            context = browser.new_context(**context_options)
            # 将 context 添加到 context 列表中进行管理
            self._context_list.append(context)
            return context

    def get_context_(self) -> list[BrowserContext]:
        """
        安全获得 context 列表，方便复用

        返回上下文实例的副本，避免直接操作内部列表。

        :return: 当前工厂管理的上下文实例列表的副本
        :raises RuntimeError: 当 PlaywrightFactory 已关闭时抛出
        """
        with self._lock:
            if not self._playwright_flag:
                raise RuntimeError("PlaywrightFactory已关闭")
            return self._context_list.copy()

    # noinspection PyMethodMayBeStatic
    def new_page(self, context: BrowserContext) -> Page:
        """
        仅提供创建 Page 的便捷方法：不登记 page，page 生命周期由 context 管理。

        :param context: 浏览器上下文实例
        :return: 新创建的 Page 实例
        """
        return context.new_page()

    def close_context(self, context: BrowserContext) -> None:
        """
        关闭单个 context（幂等操作）。

        说明：
        - 幂等操作：多次调用不会产生副作用
        - 先从registry移除，避免并发shutdown/重复close
        - 记录关闭失败的错误信息

        :param context: 要关闭的浏览器上下文实例
        """
        with self._lock:
            # 先从 registry 移除，避免并发 shutdown/重复 close
            if context in self._context_list:
                self._context_list.remove(context)

        try:
            context.close()
        except Exception as e:
            debug(f"关闭 context 失败：{e}")

    def close_browser(self, browser: Browser) -> None:
        """
        关闭单个 browser（幂等操作）。

        说明：
        - 幂等操作：多次调用不会产生副作用
        - 先从registry移除，避免并发shutdown/重复close
        - 记录关闭失败的错误信息

        :param browser: 要关闭的浏览器实例
        """
        with self._lock:
            if browser in self._browser_list:
                self._browser_list.remove(browser)

        try:
            browser.close()
        except Exception as e:
            debug(f"关闭 browser 失败：{e}")

    def close(self) -> bool:
        """
        统一回收资源（幂等操作 + 正确关闭顺序）：contexts -> browsers -> playwright.stop()

        说明：
        1. 幂等操作：多次调用不会产生副作用
        2. 严格关闭顺序：先关闭所有context，再关闭所有browser，最后停止playwright引擎
        3. 释放单例：重置单例实例，允许重新创建新的工厂实例
        4. 重置状态：将工厂标记为未初始化状态

        :return: 总是返回True，表示关闭操作已完成
        """
        with self._lock:
            if not self._playwright_flag:
                return True

            # 先置状态，阻止后续创建
            self._playwright_flag = False

            # 锁内：拷贝并清空 registry
            contexts = list(self._context_list)
            browsers = list(self._browser_list)
            self._context_list.clear()
            self._browser_list.clear()

            pw = self.playwright
            self.playwright = None  # 断开引用，避免重复 stop

        # 锁外：严格顺序
        for ctx in contexts:
            try:
                ctx.close()
            except Exception as e:
                debug(f"关闭 context 失败：{e}")

        for br in browsers:
            try:
                br.close()
            except Exception as e:
                debug(f"关闭 browser 失败：{e}")

        if pw is not None:
            try:
                pw.stop()
            except Exception as e:
                debug(f"停止 playwright 失败：{e}")

        # 释放单例
        self._initialized = False  # 可选：表示当前对象已不可用
        PlaywrightFactory._instance = None
        return True

    @contextmanager
    def managed_context(self, browser: Browser, context_options: ContextOptions | None = None):
        """
        上下文管理器，用于创建和自动清理 BrowserContext。

        说明：
        - 使用Python的上下文管理器模式，确保资源在使用后自动清理
        - 支持浏览器实例复用：如果browser参数为None，会复用第一个可用的浏览器或新建一个

        使用示例：
            with factory.managed_context() as context:
                page = context.new_page()
                page.goto("https://example.com")
            # context 在这里会自动关闭

        :param browser: 用于创建上下文的浏览器实例，如果为None则复用现有浏览器或新建
        :param context_options: 上下文配置选项，如果未提供则使用工厂默认配置
        :return: BrowserContext 实例的生成器
        """
        if browser is None:
            # 默认策略：有就复用第一个，没有就新建
            browsers = self.get_browser_()
            browser = browsers[0] if browsers else self.new_browser()
        ctx = self.new_context(browser, context_options)
        try:
            yield ctx
        finally:
            self.close_context(ctx)