# base_page_improved.py
# 内置库
import re
import time
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, List, Dict, Literal, cast
# 第三方库
from playwright.sync_api import Page, Locator, expect, Error as PlaywrightError, TimeoutError as PlaywrightTimeoutError
# 你原来的工具
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


class BasePage:
    """
    BasePage 是所有页面对象的基类，封装 Playwright Page 的通用能力。

    设计原则：
    - 所有交互都基于 Locator，而非直接传 selector 字符串（但也支持传 selector 自动封装）
    - 不包含任何业务逻辑
    - 为企业级自动化测试提供稳定、可扩展的基础能力

    :ivar page: Playwright Page 对象
    :type page: Page
    """

    def __init__(self, page: Page):
        """
        初始化 BasePage。

        :param page: Playwright 提供的 Page 实例
        :type page: Page
        """
        self.page = page

    """Helper / 转换方法"""
    def _ensure_locator(self, selector_or_locator: str | Locator, by: By | None = None, **by_kwargs: Any) -> Locator:
        """
        将输入（selector 字符串或 Locator）标准化为 Locator 对象。

        :param selector_or_locator: 可以是 Locator 或 selector 字符串
        :type selector_or_locator: Union[str, Locator]
        :param by: 显式定位方式（可选）：'role' | 'label' | 'text' | 'placeholder' | 'alt' | 'title' | 'test_id' | None
        :type by: Optional[str]
        :param by_kwargs: 当 by='role' 时可传 name=..., 或其它 get_by_xxx 的参数
        :return: 标准化后的 Locator
        :rtype: Locator

        示例：
            self._ensure_locator(page.get_by_role("button", name="登录"))  # 直接传 Locator
            self._ensure_locator("登录按钮", by="text")
            self._ensure_locator("#id")  # 默认为 page.locator(css)
        """
        if isinstance(selector_or_locator, Locator):
            return selector_or_locator

        # 显式优先调用 get_by_xxx（官方推荐以 get_by_role 为首选定位创建 Locator）
        if by:
            by = by.lower()
            if by == "role":
                # get_by_role 的第一个参数是 Role Literal，类型系统需要收窄
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
                # 注意：get_by_test_id 只接受 test_id 一个参数，不能透传 **by_kwargs
                return self.page.get_by_test_id(selector_or_locator)
            # 其它 by 不认识 -> 回退到 locator
        # 默认使用通用 locator（CSS / XPath）
        return self.page.locator(selector_or_locator)

    """页面级操作"""
    def open(self, url: str, timeout: int = 30000) -> None:
        """
        打开指定 URL。

        :param url: 目标页面 URL
        :type url: str
        :param timeout: 页面加载超时时间（毫秒）
        :type timeout: int
        """
        debug("打开 URL：%s", url)
        self.page.goto(url, timeout=timeout)

    def reload(self) -> None:
        """
        刷新当前页面。
        """
        self.page.reload()

    def current_url(self) -> str:
        """
        获取当前页面 URL。

        :return: 当前 URL
        :rtype: str
        """
        return self.page.url

    """Locator 基础动作（所有方法接收 Locator 或 selector）"""
    def click(self, target: str | Locator, by: str | None = None, timeout: int | None = None, force: bool = False, button: Literal["left", "middle", "right"] | None = None, modifiers: List[str] | None = None, position: Dict[str, int] | None = None, no_wait_after: bool = False, **kwargs: Any) -> None:
        """
        点击元素（直接封装 Locator.click，参数透传）。

        :param target: Locator 或 selector 字符串
        :type target: Union[str, Locator]
        :param by: 如果 target 为字符串，可以指定定位方式（见 _ensure_locator）
        :type by: Optional[str]
        :param timeout: 操作超时时间（毫秒）
        :type timeout: Optional[int]
        :param force: 是否强制跳过 actionability checks
        :type force: bool
        :param button: 'left' | 'right' | 'middle'
        :type button: str
        :param modifiers: 键修饰符列表，例如 ["Shift"]
        :type modifiers: Optional[List[str]]
        :param position: 点击位置字典 {"x":0,"y":0}
        :type position: Optional[Dict[str,int]]
        :param no_wait_after: 点击后不等待导航
        :type no_wait_after: bool
        """
        locator = self._ensure_locator(target, by=by)  # type: ignore[arg-type]
        debug("点击元素：%s（force=%s，button=%s）", locator, force, button)
        locator.click(timeout=timeout, force=force, button=button, modifiers=modifiers, position=position, no_wait_after=no_wait_after, **kwargs)

    def safe_click(self, target: str | Locator, by: str | None = None, wait_visible_timeout: int = 5000, retries: int = 3, retry_interval: float = 0.5, screenshot_on_failure: bool = True, screenshot_dir: str = "outputs/screenshots", **click_kwargs: Any) -> None:
        """
        更稳健的点击：先等待可见与可用（使用 web-first assertions），遇到异常会重试并可在最终失败时截图。

        :param target: Locator 或 selector
        :type target: Union[str, Locator]
        :param by: 定位方式（可选）
        :type by: Optional[str]
        :param wait_visible_timeout: 等待元素变为可见/可用的超时时间（毫秒）
        :type wait_visible_timeout: int
        :param retries: 重试次数
        :type retries: int
        :param retry_interval: 重试间隔（秒）
        :type retry_interval: float
        :param screenshot_on_failure: 最终失败时是否保存截图
        :type screenshot_on_failure: bool
        :param screenshot_dir: 截图目录
        :type screenshot_dir: str
        :param click_kwargs: 传给 Locator.click 的额外参数
        :type click_kwargs: Any
        """
        locator = self._ensure_locator(target, by=by)  # type: ignore[arg-type]
        last_error: PlaywrightError | PlaywrightTimeoutError | AssertionError | None = None

        for attempt in range(1, retries + 1):
            try:
                # 使用 expect 来等待“可见且可用”（两步）
                expect(locator).to_be_visible(timeout=wait_visible_timeout)
                # to_be_enabled 在 Assertions 中可用（用于确保元素可交互）
                try:
                    expect(locator).to_be_enabled(timeout=wait_visible_timeout)
                except (PlaywrightTimeoutError, PlaywrightError, AssertionError):
                    # 若 to_be_enabled 不适用（例如非表单可编辑元素），忽略
                    debug("to_be_enabled 不适用或未通过，继续执行。")

                # 真正点击
                locator.click(**click_kwargs)
                debug("safe_click 第 %d 次尝试成功。", attempt)
                return
            except (PlaywrightTimeoutError, PlaywrightError, AssertionError) as e:
                last_error = e
                info("safe_click 第 %d/%d 次尝试失败：%s", attempt, retries, str(e))
                time.sleep(retry_interval)

        # 如果重试后仍失败，截图并抛出
        if screenshot_on_failure:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_dir_path = Path(screenshot_dir)
            if not screenshot_dir_path.exists():
                mkdir(str(screenshot_dir_path))
            path = screenshot_dir_path / f"safe_click_failure_{ts}.png"
            try:
                self.page.screenshot(path=path)
                error("已保存失败截图：%s", str(path))
            except (PlaywrightTimeoutError, PlaywrightError) as se:
                error("截图失败：%s", str(se))

        critical("safe_click 重试全部失败，最后错误：%s", traceback.format_exc())
        raise last_error  # type: ignore[misc]

    def double_click(self, target: str | Locator, by: str | None = None, **kwargs: Any) -> None:
        """
        双击元素（Locator.dblclick）。

        :param target: Locator 或 selector
        :type target: Union[str, Locator]
        :param by: 定位方式
        :type by: Optional[str]
        """
        locator = self._ensure_locator(target, by=by)  # type: ignore[arg-type]
        locator.dblclick(**kwargs)

    def right_click(self, target: str | Locator, by: str | None = None, **kwargs: Any) -> None:
        """
        右键单击（context menu）。

        :param target: Locator 或 selector
        :type target: Union[str, Locator]
        :param by: 定位方式
        :type by: Optional[str]
        """
        self.click(target, by=by, button="right", **kwargs)

    def fill(self, target: str | Locator, text: str, by: str | None = None, timeout: int | None = None) -> None:
        """
        填充输入框（会 focus 并触发 input 事件）。推荐用法来自官方：优先 page.get_by_xxx().fill(...)

        :param target: Locator 或 selector
        :type target: Union[str, Locator]
        :param text: 要填入的文本
        :type text: str
        :param by: 定位方式
        :type by: Optional[str]
        :param timeout: 超时时间（毫秒）
        :type timeout: Optional[int]
        """
        locator = self._ensure_locator(target, by=by)  # type: ignore[arg-type]
        locator.fill(text, timeout=timeout)

    def type(self, target: str | Locator, text: str, by: str | None = None, delay: int = 50) -> None:
        """
        模拟逐字输入（当页面对按键有特殊处理时使用）。

        :param target: Locator 或 selector
        :type target: Union[str, Locator]
        :param text: 输入内容
        :type text: str
        :param by: 定位方式
        :type by: Optional[str]
        :param delay: 每字符延迟（毫秒）
        :type delay: int
        """
        locator = self._ensure_locator(target, by=by)  # type: ignore[arg-type]
        # 对于需要逐字输入的场景，官方建议使用 press_sequentially 或 type
        locator.type(text, delay=delay)

    def press(self, target: str | Locator, key: str, by: str | None = None, timeout: int | None = None) -> None:
        """
        在元素上触发键盘事件（例如 Enter、Control+ArrowRight 等）。

        :param target: Locator 或 selector
        :type target: Union[str, Locator]
        :param key: 键名，例如 "Enter" 或 "Control+ArrowRight"
        :type key: str
        :param by: 定位方式
        :type by: Optional[str]
        :param timeout: 超时时间
        :type timeout: Optional[int]
        """
        locator = self._ensure_locator(target, by=by)  # type: ignore[arg-type]
        locator.press(key, timeout=timeout)

    def press_sequentially(self, target: str | Locator, text: str, by: str | None = None, delay: int | None = None) -> None:
        """
        逐键按下（会产生完整 keydown/keyup/keypress 序列），适合需要逐键触发逻辑的场景。

        :param target: Locator 或 selector
        :type target: Union[str, Locator]
        :param text: 要发送的字符串
        :type text: str
        :param by: 定位方式
        :type by: Optional[str]
        :param delay: 可选延迟
        :type delay: Optional[int]
        """
        locator = self._ensure_locator(target, by=by)  # type: ignore[arg-type]
        # Playwright 提供 press_sequentially
        locator.press_sequentially(text) if hasattr(locator, "press_sequentially") else locator.type(text, delay=delay or 0)

    """Checkbox / Radio / Select / Upload"""
    def set_checked(self, target: str | Locator, checked: bool = True, by: str | None = None) -> None:
        """
        设置 checkbox / radio 的选中状态（使用 locator.set_checked）。

        :param target: Locator 或 selector
        :type target: Union[str, Locator]
        :param checked: True 表示选中，False 表示取消
        :type checked: bool
        :param by: 定位方式
        :type by: Optional[str]
        """
        locator = self._ensure_locator(target, by=by)  # type: ignore[arg-type]
        locator.set_checked(checked)

    def is_checked(self, target: str | Locator, by: str | None = None) -> bool:
        """
        判断 checkbox / radio 是否被选中。

        :param target: Locator 或 selector
        :type target: Union[str, Locator]
        :param by: 定位方式
        :type by: Optional[str]
        :return: True 表示已选中
        :rtype: bool
        """
        locator = self._ensure_locator(target, by=by)  # type: ignore[arg-type]
        return locator.is_checked()

    def select_option(self, target: str | Locator, value_or_values: str | List[str] | Dict[str, Any], by: str | None = None, **kwargs: Any) -> None:
        """
        在 <select> 元素上选择 option。支持 value、label 或多个值。

        :param target: Locator 或 selector
        :type target: Union[str, Locator]
        :param value_or_values: 单个 value (str) 或 value 列表，或 dict(label=...) 等
        :type value_or_values: Union[str, List[str], Dict[str, Any]]
        :param by: 定位方式
        :type by: Optional[str]
        :param kwargs: 额外透传参数
        """
        locator = self._ensure_locator(target, by=by)  # type: ignore[arg-type]
        locator.select_option(value_or_values, **kwargs)

    def upload_files(self, target: str | Locator, files: str | List[str] | List[Dict[str, Any]], by: str | None = None) -> None:
        """
        为 type=file input 设置待上传文件（支持字符串路径列表或 buffer 形式）。

        :param target: Locator 或 selector（应指向 input[type=file]）
        :type target: Union[str, Locator]
        :param files: 文件路径或 [{name, mimeType, buffer}] 形式
        :type files: Union[str, List[str], List[Dict[str, Any]]]
        :param by: 定位方式
        :type by: Optional[str]
        """
        locator = self._ensure_locator(target, by=by)  # type: ignore[arg-type]
        locator.set_input_files(files)

    """读取 / 列表操作"""
    def get_text(self, target: str | Locator, by: str | None = None) -> str:
        """
        获取元素文本（inner_text）。

        :param target: Locator 或 selector
        :type target: Union[str, Locator]
        :param by: 定位方式
        :type by: Optional[str]
        :return: 文本内容
        :rtype: str
        """
        locator = self._ensure_locator(target, by=by)  # type: ignore[arg-type]
        return locator.inner_text()

    def get_attribute(self, target: str | Locator, name: str, by: str | None = None) -> str | None:
        """
        获取元素属性值。

        :param target: Locator 或 selector
        :type target: Union[str, Locator]
        :param name: 属性名
        :type name: str
        :param by: 定位方式
        :type by: Optional[str]
        :return: 属性值
        :rtype: Optional[str]
        """
        locator = self._ensure_locator(target, by=by)  # type: ignore[arg-type]
        return locator.get_attribute(name)

    def get_value(self, target: str | Locator, by: str | None = None) -> str:
        """
        获取 input/textarea 的 value（等价于 locator.input_value）。

        :param target: Locator 或 selector
        :type target: Union[str, Locator]
        :param by: 定位方式
        :type by: Optional[str]
        :return: 输入值字符串
        :rtype: str
        """
        locator = self._ensure_locator(target, by=by)  # type: ignore[arg-type]
        return locator.input_value()

    def count(self, target: str | Locator, by: str | None = None) -> int:
        """
        返回匹配 locator 的元素数量（list 场景常用）。

        :param target: Locator 或 selector
        :type target: Union[str, Locator]
        :param by: 定位方式
        :type by: Optional[str]
        :return: 元素数量
        :rtype: int
        """
        locator = self._ensure_locator(target, by=by)  # type: ignore[arg-type]
        return locator.count()

    def all_inner_texts(self, target: str | Locator, by: str | None = None) -> List[str]:
        """
        批量获取匹配元素的 innerText 列表（更稳定且高效）。

        :param target: Locator 或 selector
        :type target: Union[str, Locator]
        :param by: 定位方式
        :type by: Optional[str]
        :return: innerText 列表
        :rtype: List[str]
        """
        locator = self._ensure_locator(target, by=by)  # type: ignore[arg-type]
        return locator.all_inner_texts()

    def all_text_contents(self, target: str | Locator, by: str | None = None) -> List[str]:
        """
        批量获取匹配元素的 textContent 列表。

        :param target: Locator 或 selector
        :type target: Union[str, Locator]
        :param by: 定位方式
        :type by: Optional[str]
        :return: textContent 列表
        :rtype: List[str]
        """
        locator = self._ensure_locator(target, by=by)  # type: ignore[arg-type]
        return locator.all_text_contents()

    """等待 / 断言 / 导航辅助"""
    def wait_for(self, target: str | Locator, by: str | None = None, state: Literal["attached", "detached", "hidden", "visible"] | None = None, timeout: int = 5000) -> None:
        """
        等待 locator 达到指定 state（'visible' | 'hidden' | 'attached' | 'detached'）。

        :param target: Locator 或 selector
        :type target: Union[str, Locator]
        :param by: 定位方式
        :type by: Optional[str]
        :param state: 等待状态
        :type state: str
        :param timeout: 超时时间（毫秒）
        :type timeout: int
        """
        locator = self._ensure_locator(target, by=by)  # type: ignore[arg-type]
        locator.wait_for(state=state, timeout=timeout)

    def expect_visible(self, target: str | Locator, by: str | None = None, timeout: int = 5000) -> None:
        """
        使用 expect 断言元素可见（web-first assertions 风格）。

        :param target: Locator 或 selector
        :type target: Union[str, Locator]
        :param by: 定位方式
        :type by: Optional[str]
        :param timeout: 超时时间
        :type timeout: int
        """
        locator = self._ensure_locator(target, by=by)  # type: ignore[arg-type]
        expect(locator).to_be_visible(timeout=timeout)

    def expect_text(self, target: str | Locator, text: str, by: str | None = None, timeout: int = 5000) -> None:
        """
        使用 expect 断言文本（完全匹配或可用正则）。

        :param target: Locator 或 selector
        :type target: Union[str, Locator]
        :param text: 期望文本
        :type text: str
        :param by: 定位方式
        :type by: Optional[str]
        :param timeout: 超时时间
        :type timeout: int
        """
        locator = self._ensure_locator(target, by=by)  # type: ignore[arg-type]
        expect(locator).to_have_text(text, timeout=timeout)

    def wait_for_url(self, url: str | re.Pattern[str], timeout: int = 30000) -> None:
        """
        等待主 frame 跳转到指定 URL 或匹配 pattern。

        :param url: URL 字符串或正则
        :type url: Union[str, re.Pattern]
        :param timeout: 超时时间（毫秒）
        :type timeout: int
        """
        self.page.wait_for_url(url, timeout=timeout)

    def wait_for_load_state(self, state: Literal["domcontentloaded", "load", "networkidle"] | None = None, timeout: int = 30000) -> None:
        """
        等待页面达到某个加载状态（'load' | 'domcontentloaded' | 'networkidle'）。
        "domcontentloaded" # DOM 加载完成
        "load"             # 页面完全加载（默认）
        "networkidle"      # 网络空闲（推荐）
        "commit"           # 收到响应头

        :param state: 加载状态
        :type state: str
        :param timeout: 超时时间（毫秒）
        :type timeout: int
        """
        self.page.wait_for_load_state(state, timeout=timeout)

    """截图 / 调试"""
    def screenshot(self, name: str, directory: str = "outputs/screenshots", full_page: bool = False) -> str:
        """
        对当前页面进行截图并保存到指定目录（带时间戳）。

        :param name: 截图文件名（不含扩展名）
        :type name: str
        :param directory: 截图保存目录
        :type directory: str
        :param full_page: 是否截取整页
        :type full_page: bool
        :return: 截图文件路径
        :rtype: str
        """
        directory_path = Path(directory)
        if not directory_path.exists():
            mkdir(str(directory_path))
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = directory_path / f"{name}_{timestamp}.png"
        self.page.screenshot(path=path, full_page=full_page)
        return str(path)

    def screenshot_element(self, target: str | Locator, name: str, directory: str = "outputs/screenshots", by: str | None = None) -> str:
        """
        对单个元素截图（Element screenshot）。

        :param target: Locator 或 selector
        :type target: Union[str, Locator]
        :param name: 文件名（不含扩展名）
        :type name: str
        :param directory: 保存目录
        :type directory: str
        :param by: 定位方式
        :type by: Optional[str]
        :return: 文件路径
        :rtype: str
        """
        locator = self._ensure_locator(target, by=by)  # type: ignore[arg-type]
        directory_path = Path(directory)
        if not directory_path.exists():
            mkdir(str(directory_path))
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = directory_path / f"{name}_{timestamp}.png"
        locator.screenshot(path=path)
        return str(path)

    def highlight(self, target: str | Locator, by: str | None = None, duration: float = 1.0) -> None:
        """
        在页面上高亮某个元素（用于调试，运行 JS 修改 style）。

        :param target: Locator 或 selector
        :type target: Union[str, Locator]
        :param by: 定位方式
        :type by: Optional[str]
        :param duration: 高亮保留时长（秒）
        :type duration: float
        """
        locator = self._ensure_locator(target, by=by)  # type: ignore[arg-type]
        # 给第一个匹配元素加样式，然后等待再去掉
        try:
            locator.evaluate(
                """el => {
                    const old = el.style.outline;
                    el.style.outline = '3px solid rgba(255,0,0,0.8)';
                    return old;
                }"""
            )
            time.sleep(duration)
            # 恢复（简单方式：再次设置 outline 为 empty）
            locator.evaluate("el => el.style.outline = ''")
        except (PlaywrightTimeoutError, PlaywrightError):
            exception("高亮元素失败。")

    """低级扩展（evaluate / element handle）"""
    def evaluate_on_locator(self, target: str | Locator, expression: str, arg: Any = None, by: str | None = None) -> Any:
        """
        在 locator 指向的元素上执行 JS 表达式 / 函数（返回值可序列化）。

        :param target: Locator 或 selector
        :type target: Union[str, Locator]
        :param expression: JS 表达式或函数体（字符串）
        :type expression: str
        :param arg: 传给 evaluate 的参数
        :type arg: Any
        :param by: 定位方式
        :type by: Optional[str]
        :return: JS 返回值
        """
        locator = self._ensure_locator(target, by=by)  # type: ignore[arg-type]
        # 若想对所有匹配节点执行，请使用 evaluate_all
        return locator.evaluate(expression, arg) if hasattr(locator, "evaluate") else locator.evaluate_all(expression, arg)

    """装饰器：方法出错时自动截图（可用于 test helper）"""
    @staticmethod
    def screenshot_on_error(directory: str = "outputs/screenshots"):
        """
        装饰器：被装饰的实例方法在抛异常时自动截图并重抛异常。

        用法：
            @BasePage.screenshot_on_error()
            def some_action(self, ...):
                ...
        """

        def decorator(func: Callable):
            def wrapper(self, *args, **kwargs):
                try:
                    return func(self, *args, **kwargs)
                except (PlaywrightTimeoutError, PlaywrightError, AssertionError):
                    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                    directory_path = Path(directory)
                    if not directory_path.exists():
                        mkdir(str(directory_path))
                    name = f"{func.__name__}_error_{ts}.png"
                    path = directory_path / name
                    try:
                        self.page.screenshot(path=path)
                        error("方法执行异常，已保存截图：%s", str(path))
                    except (PlaywrightTimeoutError, PlaywrightError):
                        exception("方法异常后截图失败。")
                    raise

            wrapper.__name__ = func.__name__
            return wrapper

        return decorator
