# base_page_improved_async.py
# 内置库
import re
import asyncio  # 引入 asyncio 用于非阻塞 sleep
import traceback
from abc import abstractmethod, ABC
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, List, Dict, Literal, cast

# 第三方库 - 切换为 async_api
from playwright.async_api import Page, Locator, expect, Error as PlaywrightError, TimeoutError as PlaywrightTimeoutError

# 你原来的工具 (假设这些工具函数是同步的，非阻塞或耗时极短，可以直接混用)
from utils.path_utils import mkdir
from utils.logger import debug, info, error, critical, exception

Role = Literal[
    "alert", "alertdialog", "application", "article", "banner", "blockquote", "button", "caption", "cell", "checkbox",
    "code", "columnheader", "combobox", "complementary", "contentinfo", "definition", "deletion", "dialog", "directory",
    "document", "emphasis", "feed", "figure", "form", "generic", "grid", "gridcell", "group", "heading", "img",
    "insertion", "link", "list", "listbox", "listitem", "log", "main", "marquee", "math", "menu", "menubar",
    "menuitem", "menuitemcheckbox", "menuitemradio", "meter", "navigation", "none", "note", "option", "paragraph",
    "presentation", "progressbar", "radio", "radiogroup", "region", "row", "rowgroup", "rowheader", "scrollbar",
    "search", "searchbox", "separator", "slider", "spinbutton", "status", "strong", "subscript", "superscript",
    "switch", "tab", "table", "tablist", "tabpanel", "term", "textbox", "time", "timer", "toolbar", "tooltip", "tree",
    "treegrid", "treeitem",
]

By = Literal["role", "label", "text", "placeholder", "alt", "title", "test_id"]


class BasePage(ABC):
    """
    BasePage 异步版本，封装 Playwright Async Page 的通用能力。
    """

    @classmethod
    async def create(cls, page: Page, *args, **kwargs):
        """
        标准的异步工厂方法。
        创建、初始化并返回一个完全就绪的页面对象。
        """
        instance = cls(page, *args, **kwargs)  # 同步构造
        await instance._async_init()           # 仅做页面导航和基本等待，异步初始化
        return instance

    def __init__(self, page: Page, *args, **kwargs):
        """
        初始化 BasePage。
        注意：__init__ 本身不能是 async 的。
        """
        self.page = page
        # 关键的状态标识（必要）
        self._is_initialized = False

    @abstractmethod
    async def _async_init(self):      # 方法名改为单下划线
        """
        子类必须实现的异步初始化方法。
        用于执行如 `page.goto()`、`wait_for_load_state()` 等操作。
        """
        pass

    async def _ensure_initialized(self):
        """
        内部守护方法。在重要业务方法开始时调用，
        确保页面已初始化，防止状态错误。
        """
        if not self._is_initialized:
            raise RuntimeError(f"页面未初始化。请使用 {self.__class__.__name__}.create() 方法创建实例。")

    """Helper / 转换方法"""

    def _ensure_locator(self, selector_or_locator: str | Locator, by: By | None = None, **by_kwargs: Any) -> Locator:
        """
        将输入标准化为 Locator 对象。
        注意：locator() 和 get_by_xxx() 在 Playwright 中是同步方法（只构建查询对象，不执行操作），
        所以此方法不需要 async/await。
        """
        if isinstance(selector_or_locator, Locator):
            return selector_or_locator

        if by:
            by = by.lower()
            if by == "role":
                return self.page.get_by_role(cast(Role, selector_or_locator), **cast(Any, by_kwargs))
            if by == "label":
                return self.page.get_by_label(selector_or_locator, **by_kwargs)
            if by == "text":
                return self.page.get_by_text(selector_or_locator, **by_kwargs)
            if by == "placeholder":
                return self.page.get_by_placeholder(selector_or_locator, **by_kwargs)
            if by == "alt":
                return self.page.get_by_alt_text(selector_or_locator, **by_kwargs)
            if by == "title":
                return self.page.get_by_title(selector_or_locator, **by_kwargs)
            if by == "test_id":
                return self.page.get_by_test_id(selector_or_locator)

        return self.page.locator(selector_or_locator)

    """页面级操作"""

    async def open(self, url: str, timeout: int = 30000) -> None:
        """异步打开指定 URL"""
        debug("打开 URL：%s", url)
        await self.page.goto(url, timeout=timeout)

    async def reload(self) -> None:
        """异步刷新当前页面"""
        await self.page.reload()

    @property
    def current_url(self) -> str:
        """
        获取当前页面 URL。
        注意：page.url 是属性不是方法，无需 await。
        """
        return self.page.url

    """Locator 基础动作"""

    async def click(self, target: str | Locator, by: str | None = None, timeout: int | None = None, force: bool = False,
                    button: Literal["left", "middle", "right"] | None = None, modifiers: List[str] | None = None,
                    position: Dict[str, int] | None = None, no_wait_after: bool = False, **kwargs: Any) -> None:
        locator = self._ensure_locator(target, by=by)
        debug("点击元素：%s（force=%s，button=%s）", locator, force, button)
        await locator.click(timeout=timeout, force=force, button=button, modifiers=modifiers, position=position,
                            no_wait_after=no_wait_after, **kwargs)

    async def safe_click(self, target: str | Locator, by: str | None = None, wait_visible_timeout: int = 5000,
                         retries: int = 3, retry_interval: float = 0.5, screenshot_on_failure: bool = True,
                         screenshot_dir: str = "outputs/screenshots", **click_kwargs: Any) -> None:
        """
        更稳健的点击（异步版）。
        """
        locator = self._ensure_locator(target, by=by)
        last_error: PlaywrightError | PlaywrightTimeoutError | AssertionError | None = None

        for attempt in range(1, retries + 1):
            try:
                # 异步 Expect 需要 await
                await expect(locator).to_be_visible(timeout=wait_visible_timeout)
                try:
                    await expect(locator).to_be_enabled(timeout=wait_visible_timeout)
                except (PlaywrightTimeoutError, PlaywrightError, AssertionError):
                    debug("to_be_enabled 不适用或未通过，继续执行。")

                await locator.click(**click_kwargs)
                debug("safe_click 第 %d 次尝试成功。", attempt)
                return
            except (PlaywrightTimeoutError, PlaywrightError, AssertionError) as e:
                last_error = e
                info("safe_click 第 %d/%d 次尝试失败：%s", attempt, retries, str(e))
                # 使用 asyncio.sleep 替代 time.sleep
                await asyncio.sleep(retry_interval)

        if screenshot_on_failure:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_dir_path = Path(screenshot_dir)
            if not screenshot_dir_path.exists():
                mkdir(str(screenshot_dir_path))
            path = screenshot_dir_path / f"safe_click_failure_{ts}.png"
            try:
                await self.page.screenshot(path=path)
                error("已保存失败截图：%s", str(path))
            except (PlaywrightTimeoutError, PlaywrightError) as se:
                error("截图失败：%s", str(se))

        critical("safe_click 重试全部失败，最后错误：%s", traceback.format_exc())
        raise last_error  # type: ignore[misc]

    async def double_click(self, target: str | Locator, by: str | None = None, **kwargs: Any) -> None:
        locator = self._ensure_locator(target, by=by)
        await locator.dblclick(**kwargs)

    async def right_click(self, target: str | Locator, by: str | None = None, **kwargs: Any) -> None:
        # 复用自身的 click 方法，需要 await
        await self.click(target, by=by, button="right", **kwargs)

    async def fill(self, target: str | Locator, text: str, by: str | None = None, timeout: int | None = None) -> None:
        locator = self._ensure_locator(target, by=by)
        await locator.fill(text, timeout=timeout)

    async def type(self, target: str | Locator, text: str, by: str | None = None, delay: int = 50) -> None:
        locator = self._ensure_locator(target, by=by)
        await locator.type(text, delay=delay)

    async def press(self, target: str | Locator, key: str, by: str | None = None, timeout: int | None = None) -> None:
        locator = self._ensure_locator(target, by=by)
        await locator.press(key, timeout=timeout)

    async def press_sequentially(self, target: str | Locator, text: str, by: str | None = None,
                                 delay: int | None = None) -> None:
        locator = self._ensure_locator(target, by=by)
        if hasattr(locator, "press_sequentially"):
            await locator.press_sequentially(text)
        else:
            await locator.type(text, delay=delay or 0)

    """Checkbox / Radio / Select / Upload"""

    async def set_checked(self, target: str | Locator, checked: bool = True, by: str | None = None) -> None:
        locator = self._ensure_locator(target, by=by)
        await locator.set_checked(checked)

    async def is_checked(self, target: str | Locator, by: str | None = None) -> bool:
        locator = self._ensure_locator(target, by=by)
        return await locator.is_checked()

    async def select_option(self, target: str | Locator, value_or_values: str | List[str] | Dict[str, Any],
                            by: str | None = None, **kwargs: Any) -> None:
        locator = self._ensure_locator(target, by=by)
        await locator.select_option(value_or_values, **kwargs)

    async def upload_files(self, target: str | Locator, files: str | List[str] | List[Dict[str, Any]],
                           by: str | None = None) -> None:
        locator = self._ensure_locator(target, by=by)
        await locator.set_input_files(files)

    """读取 / 列表操作"""

    async def get_text(self, target: str | Locator, by: str | None = None) -> str:
        locator = self._ensure_locator(target, by=by)
        return await locator.inner_text()

    async def get_attribute(self, target: str | Locator, name: str, by: str | None = None) -> str | None:
        locator = self._ensure_locator(target, by=by)
        return await locator.get_attribute(name)

    async def get_value(self, target: str | Locator, by: str | None = None) -> str:
        locator = self._ensure_locator(target, by=by)
        return await locator.input_value()

    async def count(self, target: str | Locator, by: str | None = None) -> int:
        locator = self._ensure_locator(target, by=by)
        return await locator.count()

    async def all_inner_texts(self, target: str | Locator, by: str | None = None) -> List[str]:
        locator = self._ensure_locator(target, by=by)
        return await locator.all_inner_texts()

    async def all_text_contents(self, target: str | Locator, by: str | None = None) -> List[str]:
        locator = self._ensure_locator(target, by=by)
        return await locator.all_text_contents()

    """等待 / 断言 / 导航辅助"""

    async def wait_for(self, target: str | Locator, by: str | None = None,
                       state: Literal["attached", "detached", "hidden", "visible"] | None = None,
                       timeout: int = 5000) -> None:
        locator = self._ensure_locator(target, by=by)
        await locator.wait_for(state=state, timeout=timeout)

    async def expect_visible(self, target: str | Locator, by: str | None = None, timeout: int = 5000) -> None:
        locator = self._ensure_locator(target, by=by)
        # 异步 expect 必须 await
        await expect(locator).to_be_visible(timeout=timeout)

    async def expect_text(self, target: str | Locator, text: str, by: str | None = None, timeout: int = 5000) -> None:
        locator = self._ensure_locator(target, by=by)
        await expect(locator).to_have_text(text, timeout=timeout)

    async def wait_for_url(self, url: str | re.Pattern[str], timeout: int = 30000) -> None:
        await self.page.wait_for_url(url, timeout=timeout)

    async def wait_for_load_state(self, state: Literal["domcontentloaded", "load", "networkidle"] | None = None,
                                  timeout: int = 30000) -> None:
        await self.page.wait_for_load_state(state, timeout=timeout)

    """截图 / 调试"""

    async def screenshot(self, name: str, directory: str = "outputs/screenshots", full_page: bool = False) -> str:
        directory_path = Path(directory)
        if not directory_path.exists():
            mkdir(str(directory_path))
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = directory_path / f"{name}_{timestamp}.png"
        await self.page.screenshot(path=path, full_page=full_page)
        return str(path)

    async def screenshot_element(self, target: str | Locator, name: str, directory: str = "outputs/screenshots",
                                 by: str | None = None) -> str:
        locator = self._ensure_locator(target, by=by)
        directory_path = Path(directory)
        if not directory_path.exists():
            mkdir(str(directory_path))
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = directory_path / f"{name}_{timestamp}.png"
        await locator.screenshot(path=path)
        return str(path)

    async def highlight(self, target: str | Locator, by: str | None = None, duration: float = 1.0) -> None:
        locator = self._ensure_locator(target, by=by)
        try:
            await locator.evaluate(
                """el => {
                    const old = el.style.outline;
                    el.style.outline = '3px solid rgba(255,0,0,0.8)';
                    return old;
                }"""
            )
            # 异步 sleep
            await asyncio.sleep(duration)
            await locator.evaluate("el => el.style.outline = ''")
        except (PlaywrightTimeoutError, PlaywrightError):
            exception("高亮元素失败。")

    """低级扩展"""

    async def evaluate_on_locator(self, target: str | Locator, expression: str, arg: Any = None,
                                  by: str | None = None) -> Any:
        locator = self._ensure_locator(target, by=by)
        if hasattr(locator, "evaluate"):
            return await locator.evaluate(expression, arg)
        else:
            return await locator.evaluate_all(expression, arg)

    """装饰器：方法出错时自动截图"""

    @staticmethod
    def screenshot_on_error(directory: str = "outputs/screenshots"):
        """
        装饰器（异步版）：被装饰的 async 方法在抛异常时自动截图。
        """

        def decorator(func: Callable):
            # 这里的 wrapper 必须是 async 的
            async def wrapper(self, *args, **kwargs):
                try:
                    return await func(self, *args, **kwargs)
                except (PlaywrightTimeoutError, PlaywrightError, AssertionError):
                    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                    directory_path = Path(directory)
                    if not directory_path.exists():
                        mkdir(str(directory_path))
                    name = f"{func.__name__}_error_{ts}.png"
                    path = directory_path / name
                    try:
                        # 装饰器内的 self 即 BasePage 实例，调用其异步截图方法
                        await self.page.screenshot(path=path)
                        error("方法执行异常，已保存截图：%s", str(path))
                    except (PlaywrightTimeoutError, PlaywrightError):
                        exception("方法异常后截图失败。")
                    raise

            wrapper.__name__ = func.__name__
            return wrapper

        return decorator