"""
Playwright 工厂 & 管理封装

职责：
- 统一启动 / 关闭 Playwright
- 按 env.yaml & settings.yaml 配置启动浏览器
- 提供 Browser / Context / Page 获取与创建方法
"""

# 系统库
from __future__ import annotations # 解决3.7 - 3.9的py版本传递自身抛出错误问题
from pathlib import Path
from typing import Any, Dict, Optional, Generator
# 第三方库
import yaml
from playwright.sync_api import sync_playwright, Playwright, Browser, BrowserContext, Page
# 自己的模块
from utils import warning


def _load_yaml(path: Path) -> Dict[str, Any]:
    """安全读取 YAML 文件，若不存在则返回空 dict。"""
    if not path.exists():
        warning("配置文件不存在：%s，使用默认配置", path)
        return {}
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _project_root() -> Path:
    """
    从当前文件相对定位项目根目录。
    当前文件位于：utils/playwright_factory.py
    项目根目录为：Playwright个人研究成果/
    """
    return Path(__file__).resolve().parents[1]


class PlaywrightFactory:
    """
    Playwright 浏览器 / 上下文 / 页面 工厂类（同步版）

    一般用法示例（在测试代码中）：

        factory = PlaywrightFactory.get_instance()
        factory.start()  # 测试运行前启动一次

        page = factory.new_page()
        page.goto("/")

        # 所有用例结束后关闭
        factory.stop()
    """

    _instance: Optional["PlaywrightFactory"] = None

    def __init__(
        self, env_config_path: Optional[Path] = None, settings_path: Optional[Path] = None,) -> None:
        root = _project_root()

        self.env_config_path = env_config_path or root / "config" / "env.yaml"
        self.settings_path = settings_path or root / "config" / "settings.yaml"

        self.env_config: Dict[str, Any] = _load_yaml(self.env_config_path)
        self.settings: Dict[str, Any] = _load_yaml(self.settings_path)

        self._playwright: Optional[Playwright] = None
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None

        logger.info(
            "PlaywrightFactory 初始化完成。env_config=%s, settings=%s",
            self.env_config_path,
            self.settings_path,
        )

    # -------------------------------------------------------------------------
    # 单例获取
    # -------------------------------------------------------------------------
    @classmethod
    def get_instance(cls) -> "PlaywrightFactory":
        """
        简单单例，方便在多处直接调用：
            from utils.playwright_factory import PlaywrightFactory
            factory = PlaywrightFactory.get_instance()
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    # -------------------------------------------------------------------------
    # 生命周期管理
    # -------------------------------------------------------------------------
    def start(self) -> None:
        """启动 Playwright & 浏览器（若尚未启动）。"""
        if self._playwright is None:
            logger.info("启动 Playwright ...")
            self._playwright = sync_playwright().start()

        if self._browser is None:
            self._browser = self._launch_browser()

        if self._context is None:
            self._context = self._new_context_internal()

    def stop(self) -> None:
        """关闭 Page / Context / Browser / Playwright。"""
        logger.info("关闭 Playwright 相关资源 ...")

        # 顺序：page -> context -> browser -> playwright
        if self._page is not None:
            try:
                self._page.close()
            except Exception as e:  # noqa: BLE001
                logger.warning("关闭 page 失败：%s", e)
        self._page = None

        if self._context is not None:
            try:
                self._context.close()
            except Exception as e:  # noqa: BLE001
                logger.warning("关闭 context 失败：%s", e)
        self._context = None

        if self._browser is not None:
            try:
                self._browser.close()
            except Exception as e:  # noqa: BLE001
                logger.warning("关闭 browser 失败：%s", e)
        self._browser = None

        if self._playwright is not None:
            try:
                self._playwright.stop()
            except Exception as e:  # noqa: BLE001
                logger.warning("停止 playwright 失败：%s", e)
        self._playwright = None

    # -------------------------------------------------------------------------
    # 内部启动逻辑
    # -------------------------------------------------------------------------
    def _launch_browser(self) -> Browser:
        """根据 env.yaml 中配置启动浏览器。"""
        assert self._playwright is not None, "请先调用 start() 再使用浏览器"

        browser_cfg: Dict[str, Any] = self.env_config.get("browser", {})

        browser_type = browser_cfg.get("type", "chromium")  # chromium / firefox / webkit
        headless = browser_cfg.get("headless", True)
        slow_mo = browser_cfg.get("slow_mo", 0)
        args = browser_cfg.get("args", []) or []

        viewport_cfg = browser_cfg.get("viewport", {})
        viewport = {
            "width": viewport_cfg.get("width", 1280),
            "height": viewport_cfg.get("height", 720),
        }

        logger.info(
            "启动浏览器：type=%s, headless=%s, viewport=%s, slow_mo=%s",
            browser_type,
            headless,
            viewport,
            slow_mo,
        )

        if browser_type == "firefox":
            browser_type_impl = self._playwright.firefox
        elif browser_type == "webkit":
            browser_type_impl = self._playwright.webkit
        else:
            browser_type_impl = self._playwright.chromium

        browser = browser_type_impl.launch(
            headless=headless,
            slow_mo=slow_mo,
            args=args,
        )
        return browser

    def _new_context_internal(self) -> BrowserContext:
        """根据 env.yaml & settings.yaml 创建 BrowserContext。"""
        assert self._browser is not None, "浏览器尚未启动"

        context_cfg: Dict[str, Any] = self.env_config.get("context", {})
        settings_cfg: Dict[str, Any] = self.settings.get("playwright", {})

        # 超时相关（settings.yaml 中 playwight.action_timeout / navigation_timeout 等）
        default_timeout = settings_cfg.get("action_timeout", 10_000)  # ms
        navigation_timeout = settings_cfg.get("navigation_timeout", 30_000)  # ms

        viewport_cfg = self.env_config.get("browser", {}).get("viewport", {})
        viewport_size = {
            "width": viewport_cfg.get("width", 1280),
            "height": viewport_cfg.get("height", 720),
        }

        record_video_dir = context_cfg.get("record_video_dir")  # 如：outputs/videos
        record_video_size = context_cfg.get("record_video_size")  # dict: {width, height}

        trace_cfg = context_cfg.get("trace", "off")  # on/off/retain-on-failure

        context_kwargs: Dict[str, Any] = {
            "viewport": viewport_size,
        }

        if record_video_dir:
            # 统一用相对项目根目录的路径
            video_dir = _project_root() / record_video_dir
            video_dir.mkdir(parents=True, exist_ok=True)
            context_kwargs["record_video_dir"] = str(video_dir)

        if record_video_size:
            context_kwargs["record_video_size"] = record_video_size

        context = self._browser.new_context(**context_kwargs)
        context.set_default_timeout(default_timeout)
        context.set_default_navigation_timeout(navigation_timeout)

        # trace 设置（启用 trace 会影响性能，按需开启）
        if trace_cfg and trace_cfg != "off":
            try:
                context.tracing.start(
                    screenshots=True,
                    snapshots=True,
                    sources=True,
                )
                logger.info("Trace 已开启，策略：%s", trace_cfg)
            except Exception as e:  # noqa: BLE001
                logger.warning("开启 trace 失败：%s", e)

        return context

    # -------------------------------------------------------------------------
    # 对外公开 API
    # -------------------------------------------------------------------------
    @property
    def base_url(self) -> str:
        """从 env.yaml 中读取 base_url。"""
        return self.env_config.get("base_url", "").rstrip("/")

    @property
    def playwright(self) -> Playwright:
        assert self._playwright is not None, "Playwright 尚未启动，请先调用 start()"
        return self._playwright

    @property
    def browser(self) -> Browser:
        assert self._browser is not None, "Browser 尚未启动，请先调用 start()"
        return self._browser

    @property
    def context(self) -> BrowserContext:
        if self._context is None:
            self._context = self._new_context_internal()
        return self._context

    def new_context(self, **kwargs: Any) -> BrowserContext:
        """
        创建一个新的 BrowserContext（独立会话）。
        一般在多用例隔离或多用户场景下使用。
        """
        assert self._browser is not None, "Browser 尚未启动，请先调用 start()"
        ctx = self._browser.new_context(**kwargs)
        return ctx

    def get_page(self) -> Page:
        """获取当前单例 context 中的 page，没有则创建一个。"""
        if self._page is None:
            self._page = self.context.new_page()
        return self._page

    def new_page(self, context: Optional[BrowserContext] = None) -> Page:
        """
        在指定 context 下创建一个新 page。
        若未指定 context，则使用默认单例 context。
        """
        ctx = context or self.context
        return ctx.new_page()

    # -------------------------------------------------------------------------
    # 上下文管理器辅助：with factory.page_session() as page: ...
    # -------------------------------------------------------------------------
    def page_session(self) -> Generator[Page, None, None]:
        """
        一个简单的 generator，用于 with 语法：
            factory = PlaywrightFactory.get_instance()
            factory.start()

            with factory.page_session() as page:
                page.goto("...")

        结束时自动关闭该 page（不影响全局 browser/context）。
        """
        page = self.new_page()
        try:
            yield page
        finally:
            try:
                page.close()
            except Exception as e:  # noqa: BLE001
                logger.warning("关闭 page 失败：%s", e)

