"""base_page.py
该类的主要作用是封装 WebDriver 的初始化、配置、以及常用的浏览器和元素操作方法，
为上层的具体业务页面对象（Page Object）提供一个稳定、健壮和可复用的基类。
它实现了对 Selenium 复杂 API 的简化和异常处理，
遵循了 Page Object Model（PO模型）中“将底层操作细节与上层业务逻辑分离”的原则。
"""
# 内置库
import json
from time import sleep

# 第三方库
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import ActionChains  # 行为链
from selenium.webdriver.common.by import By  # 元素定位策略
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.common import TimeoutException, NoSuchElementException, StaleElementReferenceException, \
    ElementNotInteractableException, InvalidCookieDomainException


class BasePage:
    def __init__(self, driver: webdriver.Chrome):
        """封装selenium的基础的行为

        1: By.CSS_SELECTOR      - 性能好，写法灵活，推荐
        2: By.ID                - 性能最佳，元素唯一时首选
        3: By.XPATH             - 功能强大，可遍历DOM，但性能相对较差
        4: By.NAME              - 主要用于表单元素
        5: By.CLASS_NAME        - 按CSS类名定位
        6: By.LINK_TEXT         - 精确匹配超链接文本
        7: By.PARTIAL_LINK_TEXT - 部分匹配超链接文本
        8: By.TAG_NAME          - 按HTML标签名定位
        :param driver: 谷歌浏览器驱动对象
        """
        # 驱动器对象
        self.driver: webdriver.Chrome = driver

        # 定位策略
        self.by_mapping: dict = {
            1: By.CSS_SELECTOR,  # CSS选择器，灵活、性能最佳
            2: By.ID,  # 最快速，但是ID有可能会变（如果确认ID就不管了）
            3: By.XPATH,  # 可能会变位置，
            4: By.NAME,  # 表单元素的名称，除表单外不一定有
            5: By.CLASS_NAME,  # 样式类
            6: By.LINK_TEXT,  # 精确的链接文本
            7: By.PARTIAL_LINK_TEXT,  # 模糊链接文本
            8: By.TAG_NAME,  # 标签名
        }

    """==============================================浏览器基础行为封装=============================================="""

    """元素查找、改变（包括元素属性查找）"""
    def wait_element_appear(self, by_value: str, mode: int = 3, timeout: int = 10):
        """等待元素出现，肉眼可见且存在DOM（有些元素不可见或无法交互不能使用该方法）
        参数直接自定义搜索策略和等待时间更加灵活，但是对象开销也会大

        1: By.CSS_SELECTOR      - 性能好，写法灵活，推荐
        2: By.ID                - 性能最佳，元素唯一时首选
        3: By.XPATH             - 功能强大，可遍历DOM，但性能相对较差
        4: By.NAME              - 主要用于表单元素
        5: By.CLASS_NAME        - 按CSS类名定位
        6: By.LINK_TEXT         - 精确匹配超链接文本
        7: By.PARTIAL_LINK_TEXT - 部分匹配超链接文本
        8: By.TAG_NAME          - 按HTML标签名定位
        :param by_value: 需要寻找元素的by方法的值
        :param mode: 搜索模式（by_mapping），默认3
        :param timeout: 最大等待时间（默认10）
        :return: 最大等待时间内寻找到元素返回 WebElement 否则返回 False

        """
        try:
            # 创建显式等待对象
            web_driver_wait = WebDriverWait(self.driver, timeout)  # 使用默认值为10
            # 0.5秒监测元素出现
            element = web_driver_wait.until(
                # 元素可见但不一定能被点击
                expected_conditions.visibility_of_element_located((self.by_mapping[mode], by_value))
            )
            return element  # 返回找到的元素
        except TimeoutException:  # 捕获超时异常
            return False  # 直接返回false

    def wait_class_change(self, by_value: str, class_value: str, mode: int = 1, timeout: int = 10) -> bool:
        """
        检测元素样式是否改变，如果中途元素本身改变也视为css发生了变化。灵活配置定位策略和等待时间
        :param class_value: class改变后属性值（例如："video-like video-toolbar-left-item on"）
        :param by_value: 定位符
        :param mode: 定位策略
        :param timeout: 最大等待时间（秒）
        :return: 样式改变返回 True，否则返回 False
        """
        try:
            web_driver_wait = WebDriverWait(self.driver, timeout)
            # 使用 lambda 表达式作为自定义条件
            web_driver_wait.until(
                lambda driver: driver.find_element(self.by_mapping[mode], by_value).get_attribute(
                    "class") != class_value
            )
            return True
        except TimeoutException:
            return False
        except (NoSuchElementException, StaleElementReferenceException):
            # 如果元素在等待过程中消失，也认为状态已改变
            return True

    def get_text(self, by_value: str, mode: int = 1, timeout: int = 10):
        """
        安全的获得控件的文本（js刷新网页导致拿到的元素对象失效无法调用text属性）
        :param by_value: 需要寻找元素的by方法的值
        :param mode: 模式默认为1（xpath, CSS_SELECTOR, ID, NAME）
        :param timeout: 最大等待时间（默认10）
        :return: 10秒内寻找到元素返回文本 str 否则返回 False
        """

        def call_text():
            """不断获得属性"""
            try:
                # 元素存在
                element = self.wait_element_appear(by_value, mode, timeout)
                if element:
                    return element.text
                else:
                    return False
            except StaleElementReferenceException:
                return call_text()  # 捕获异常并再次尝试

        return call_text()

    """鼠标事件"""
    def click(self, by_value: str, mode: int = 3):
        """
        二次封装selenium的click方法（捕获错误），自定义捕获策略

        1: By.CSS_SELECTOR      - 性能好，写法灵活，推荐
        2: By.ID                - 性能最佳，元素唯一时首选
        3: By.XPATH             - 功能强大，可遍历DOM，但性能相对较差
        4: By.NAME              - 主要用于表单元素
        5: By.CLASS_NAME        - 按CSS类名定位
        6: By.LINK_TEXT         - 精确匹配超链接文本
        7: By.PARTIAL_LINK_TEXT - 部分匹配超链接文本
        8: By.TAG_NAME          - 按HTML标签名定位
        :param by_value:定位符
        :param mode:定位策略，默认为3
        :return:执行成功返回被点击元素 WebElement，没有元素返回 False

        """
        try:
            element = self.driver.find_element(self.by_mapping[mode], by_value)  # 找到元素
            element.click()  # 点击元素
            return element
        except NoSuchElementException:
            # 找不到元素异常
            return False

    def js_click(self, by_value: str, mode: int = 3):
        """
        点击（js注入的方式实现），出现遮罩无法点击的情况（在B站被ban了）,自定义定位模式

        1: By.CSS_SELECTOR      - 性能好，写法灵活，推荐
        2: By.ID                - 性能最佳，元素唯一时首选
        3: By.XPATH             - 功能强大，可遍历DOM，但性能相对较差
        4: By.NAME              - 主要用于表单元素
        5: By.CLASS_NAME        - 按CSS类名定位
        6: By.LINK_TEXT         - 精确匹配超链接文本
        7: By.PARTIAL_LINK_TEXT - 部分匹配超链接文本
        8: By.TAG_NAME          - 按HTML标签名定位
        :param by_value:定位符
        :param mode:定位策略，默认3
        :return:执行成功返回被点击元素 WebElement，没有元素返回 False
        """
        try:
            element = self.driver.find_element(self.by_mapping[mode], by_value)  # 找到元素
            self.driver.execute_script("arguments[0].click();", element)  # 点击元素
            return element
        except NoSuchElementException:
            # 找不到元素异常
            return False

    def wait_click(self, by_value: str, mode: int = 1, timeout: int = 10):
        """
        等待元素出现并点击（selenium的click），参数直接自定义搜索策略和等待时间更加灵活，但是对象开销也会大

        1: By.CSS_SELECTOR      - 性能好，写法灵活，推荐
        2: By.ID                - 性能最佳，元素唯一时首选
        3: By.XPATH             - 功能强大，可遍历DOM，但性能相对较差
        4: By.NAME              - 主要用于表单元素
        5: By.CLASS_NAME        - 按CSS类名定位
        6: By.LINK_TEXT         - 精确匹配超链接文本
        7: By.PARTIAL_LINK_TEXT - 部分匹配超链接文本
        8: By.TAG_NAME          - 按HTML标签名定位
        :param by_value:定位符
        :param mode:定位策略
        :param timeout: 元素出现最大等待时间（默认10）
        :return:执行成功返回元素对象 WebElement，未找到元素（超时）返回 False
        """
        try:
            # 创建 WebDriverWait 实例，设置最大等待时间
            web_driver_wait = WebDriverWait(self.driver, timeout)
            element = web_driver_wait.until(
                # 确保元素可见且能被点击
                expected_conditions.element_to_be_clickable((self.by_mapping[mode], by_value))
            )
        except TimeoutException:  # 捕获超时异常
            return False  # 直接返回false
        # # 滚动视窗到该元素上()click自带了
        # self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        # sleep(1)
        element.click()  # 点击
        return element  # 返回找到的元素

    def js_wait_click(self, by_value: str, mode: int = 1, timeout: int = 10):
        """
        等待元素出现并点击（js注入的方式），自定义定位策略和时间，对象额外开销
        :param by_value:定位符
        :param mode:定位策略
        :param timeout: 元素出现最大等待时间（默认10）
        :return:执行成功返回元素对象 WebElement，未找到元素（超时）返回 False
        """
        try:
            # 创建 WebDriverWait 实例，设置最大等待时间
            web_driver_wait = WebDriverWait(self.driver, timeout)
            # 使用 until() 方法和 EC.presence_of_element_located 条件(元素出现且能被点击)
            element = web_driver_wait.until(
                expected_conditions.element_to_be_clickable((self.by_mapping[mode], by_value))
            )
        except TimeoutException:  # 捕获超时异常
            return False  # 直接返回false
        # 滚动视窗到该元素上
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        # 点击
        self.driver.execute_script("arguments[0].click();", element)
        return element  # 返回找到的元素

    def wait_double_click(self, by_value: str, mode: int = 1, timeout: int = 10):
        """
        等待元素出现并点击（selenium的click）,灵活控制

        1: By.CSS_SELECTOR      - 性能好，写法灵活，推荐
        2: By.ID                - 性能最佳，元素唯一时首选
        3: By.XPATH             - 功能强大，可遍历DOM，但性能相对较差
        4: By.NAME              - 主要用于表单元素
        5: By.CLASS_NAME        - 按CSS类名定位
        6: By.LINK_TEXT         - 精确匹配超链接文本
        7: By.PARTIAL_LINK_TEXT - 部分匹配超链接文本
        8: By.TAG_NAME          - 按HTML标签名定位
        :param by_value:定位符
        :param mode:定位策略
        :param timeout: 元素出现最大等待时间（默认10）
        :return:执行成功返回元素对象 WebElement，未找到元素（超时）返回 False
        """
        try:
            # 创建 WebDriverWait 实例，设置最大等待时间
            web_driver_wait = WebDriverWait(self.driver, timeout)
            # 使用 until() 方法和 EC.presence_of_element_located 条件(元素出现在 DOM 结构中，但不一定可见)
            element = web_driver_wait.until(
                # 确保元素可见且能被点击
                expected_conditions.element_to_be_clickable((self.by_mapping[mode], by_value))

            )
        except TimeoutException:  # 捕获超时异常
            return False  # 直接返回false
        # 滚动视窗到该元素上
        # self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        # 双击
        ActionChains(self.driver).double_click(element).perform()
        return element  # 返回找到的元素

    def right_click(self, element: WebElement):
        """
        右击行为封装
        :param element:定位符
        :return:执行成功返回被点击元素 WebElement，没有元素返回 False
        """
        try:
            ActionChains(self.driver).context_click(element).perform()
            return element
        except NoSuchElementException:
            # 找不到元素异常
            return False

    def wait_right_click(self, by_value: str) -> bool:
        """
        最大时间等待元素出现并右击
        :param by_value:定位符
        :return: 成功返回True，否则返回False
        """
        # 判断元素是否存在
        element = self.wait_element_appear(by_value)
        if element:
            self.right_click(element)
            return True
        return False

    def middle_click(self, element: WebElement) -> bool:
        """
        使用js的方式实现
        :param element:被操作的元素
        :return: bool
        """
        try:
            # 滚动视窗到该元素上
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            # 点击
            self.driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {button: 1}));", element)
            return True
        except (NoSuchElementException, ElementNotInteractableException):
            return False

    def move(self, element: WebElement) -> bool:
        """
        鼠标移动（悬停）都某个元素上
        :param element:被操作的元素
        :return: 悬停返回True，元素消失或被遮挡或不可交互返回False
        """
        try:
            # 执行移动（悬停）操作
            ActionChains(self.driver).move_to_element(element).perform()
            return True
        except (NoSuchElementException, ElementNotInteractableException):
            return False

    def wait_move(self, by_value: str) -> bool:
        """
        等待某个元素出现并把鼠标移动（悬停）在这个元素上，最大时间全局定义
        :param by_value:定位符
        :return: 悬停返回True，最大时间内元素未找到消失或被遮挡或不可交互返回False
        """
        # 判断元素是否存在
        element = self.wait_element_appear(by_value)
        if element:
            # 执行悬停操作
            return self.move(element)
        return False

    def hold(self, element: WebElement) -> bool:
        """
        鼠标按住某个元素
        :param element: 被操作的元素
        :return: 成功按住返回True, 最大时间内元素未找到消失或被遮挡或不可交互返回False
        """
        try:
            # 点击和按住
            ActionChains(self.driver).click_and_hold(element).perform()
            return True
        except (NoSuchElementException, ElementNotInteractableException):
            return False

    def wait_hold(self, by_value: str) -> bool:
        """
        等待某个元素出现并把按住这个元素，最大时间全局定义
        :param by_value:定位符
        :return: 悬停返回True，最大时间内元素未找到消失或被遮挡或不可交互返回False
        """
        # 判断元素是否存在
        element = self.wait_element_appear(by_value)
        if element:
            # 执行按住操作
            return self.hold(element)
        return False

    def release_actions(self):
        """
        清除所有行为
        :return: True
        """
        ActionBuilder(self.driver).clear_actions()
        return True

    """键盘事件"""
    def send_key(self, by_value: str, mode: int = 3, timeout: int = 10, *keys_to_send: str):
        """
        设定时间内等待元素出现点击后输入多个字符(键盘的值或文本)，自定义超时时间和搜索策略

        1: By.CSS_SELECTOR      - 性能好，写法灵活，推荐
        2: By.ID                - 性能最佳，元素唯一时首选
        3: By.XPATH             - 功能强大，可遍历DOM，但性能相对较差
        4: By.NAME              - 主要用于表单元素
        5: By.CLASS_NAME        - 按CSS类名定位
        6: By.LINK_TEXT         - 精确匹配超链接文本
        7: By.PARTIAL_LINK_TEXT - 部分匹配超链接文本
        8: By.TAG_NAME          - 按HTML标签名定位
        :param by_value:定位符
        :param mode: 搜索模式（by_mapping），默认3
        :param keys_to_send:一个或多个字符串
        :param timeout: 最大等待时间（默认10）
        :return: 执行成功返回被点击元素 WebElement，(没有找到、无法接收输入、状态变化)返回 False
        """
        try:
            # 创建显式等待对象
            web_driver_wait = WebDriverWait(self.driver, timeout)  # 使用默认值为10
            # 0.5秒监测元素出现
            element = web_driver_wait.until(
                # 元素可见但不一定能被点击
                expected_conditions.visibility_of_element_located((self.by_mapping[mode], by_value))
            )
            element.click()  # 点击元素
            ActionChains(self.driver).send_keys(*keys_to_send).perform()  # 执行输入行为
            return element
        except (ElementNotInteractableException, StaleElementReferenceException, NoSuchElementException,
                TimeoutException):
            return False  # 失败异常

    """窗口控制类型"""

    def max_win(self):
        """
        最大化浏览器窗口
        :return: True
        """
        self.driver.maximize_window()
        return True

    def min_win(self):
        """
        最小化浏览器窗口
        :return: True
        """
        self.driver.minimize_window()

    def close_win(self, target_window_handle: str) -> bool:
        """
        关闭指定的窗口(标签页)，selenium没有给，这里实际上是跳转到该窗口（标签页）再关闭
        :param target_window_handle: 目标窗口（标签页）的句柄
        :return: 没有可以关闭或不存在窗口（标签页）返回False,成功跳转目标窗口（标签页）返回True
        """
        if self.switch_win(target_window_handle):
            self.driver.close()
            return True
        return False

    def back_win(self) -> None:
        """
        回退上一个网页
        :return: None
        """
        self.driver.back()

    def forward_win(self) -> None:
        """
        向下一个网页
        :return: None
        """
        self.driver.forward()

    def wait_win_ready(self, timeout: int = 10):
        """
        等待界面元素加载完成（使用显式等待检查 document.readyState 是否为 'complete'）,完成后也会等待1秒
        :param timeout: 最大等待时间（秒，默认为 10）
        :return: 超时返回False，准备好返回True
        """
        try:
            # 创建 WebDriverWait 实例
            web_driver_wait = WebDriverWait(self.driver, timeout)
            # 使用 lambda 表达式作为自定义条件：
            web_driver_wait.until(
                # 驱动对象是默认传递的第一个参数
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            sleep(1)    # 休眠1秒
            return True
        except TimeoutException:
            return False

    def wait_win_ex(self, win_num: int, timeout: int = 5) -> bool:
        """
        在指定时间内等待新窗口出现，等待时间自定义
        :param win_num: 原来窗口的数量（新开窗口前保存这个值），len(driver.window_handles)
        :param timeout: 最大等待时间（秒，默认为 5）
        :return: 最大时间内出现新窗口返回 True，超时返回 False
        """
        try:
            # 创建 WebDriverWait 实例
            web_driver_wait = WebDriverWait(self.driver, timeout)
            # 使用 lambda 表达式作为自定义条件：
            web_driver_wait.until(
                lambda driver: len(driver.window_handles) >= win_num
            )
            return True
        except TimeoutException:
            # 如果超过 timeout 时间窗口数量仍不足 2
            return False

    def switch_different_win(self, win_num: int, timeout: int = 5) -> bool:
        """
        切换到不是当前窗口的窗口（切换后等待1秒，不等待找不到元素）
        :param win_num: 原来窗口的数量（新开窗口前保存这个值），len(driver.window_handles)
        :param timeout: 最大等待时间（秒，默认为 5）
        :return: 最大时间内出现新窗口返回 True，超时返回 False
        """
        # 判断是否有新标签页
        if self.wait_win_ex(win_num, timeout):
            # 遍历所有句柄
            for handle in self.driver.window_handles:
                # 不是当前窗口句柄
                if handle != self.driver.current_window_handle:
                    self.driver.switch_to.window(handle)    # 跳转
                    # sleep(1)
            else:
                # 新标签页突然消失
                return False
        return True

    def switch_current_win(self):
        """
        切换到当前的窗口（点击后跳转新标签页，但是驱动没有跳过去）
        :return: 当前窗口句柄
        """
        self.driver.switch_to.window(self.driver.current_window_handle)
        return self.driver.current_window_handle

    def switch_win(self, target_window_handle: str) -> bool:
        """
        切换到新的窗口(标签页)
        :param target_window_handle: 目标窗口（标签页）的句柄
        :return: 没有跳转窗口（标签页）返回False,成功跳转目标窗口（标签页）返回True
        """
        # 遍历句柄并跳转到非原来标签页的句柄
        for window_handle in self.driver.window_handles:
            if window_handle == target_window_handle:
                # 切换到新的标签页上
                self.driver.switch_to.window(window_handle)
                # 成功跳转新的标签页
                return True
        # 没有新的标签页
        return False

    def switch_win_for_url(self, url: str) -> bool:
        """
        切换到指定url的窗口(标签页)，没有找到会跳回最开始的窗口(标签页)
        :param url: 目标窗口（标签页）的url
        :return: 没有跳转窗口（标签页）返回False,成功跳转目标窗口（标签页）返回True
        """
        # 记录最开始的窗口句柄
        original_window_handle = self.driver.current_window_handle
        # 遍历句柄并跳转标签页
        for window_handle in self.driver.window_handles:
            # 切换到新的标签页上
            self.driver.switch_to.window(window_handle)
            if self.driver.current_url == url:
                # 成功跳转指定的标签页
                return True
        # 跳回最开始的标签页
        self.driver.switch_to.window(original_window_handle)
        # 没有新的标签页
        return False

    def switch_win_for_title(self, window_title: str) -> bool:
        """
        根据标题切换到新的窗口(标签页)，没有找到会跳回最开始的窗口(标签页)
        :param window_title: 目标窗口（标签页）的标题
        :return: 没有跳转窗口（标签页）返回False,成功跳转目标窗口（标签页）返回True
        """
        # 记录最开始的窗口句柄
        original_window_handle = self.driver.current_window_handle
        # 遍历句柄并跳转标签页
        for window_handle in self.driver.window_handles:
            # 切换到新的标签页上
            self.driver.switch_to.window(window_handle)
            if self.driver.title == window_title:
                # 成功跳转指定的标签页
                return True
        # 跳回最开始的标签页
        self.driver.switch_to.window(original_window_handle)
        # 没有新的标签页
        return False

    def switch_win_for_element(self, by_value: str, mode: int = 3, timeout: int = 10) -> bool:
        """
        根据元素定位符切换到新的窗口(标签页)，没有找到会跳回最开始的窗口(标签页)。某些界面会存在特定元素，结构化定位。
        须确保网页元素加载完成，因为判定条件是特定元素存在

        1: By.CSS_SELECTOR      - 性能好，写法灵活，推荐
        2: By.ID                - 性能最佳，元素唯一时首选
        3: By.XPATH             - 功能强大，可遍历DOM，但性能相对较差
        4: By.NAME              - 主要用于表单元素
        5: By.CLASS_NAME        - 按CSS类名定位
        6: By.LINK_TEXT         - 精确匹配超链接文本
        7: By.PARTIAL_LINK_TEXT - 部分匹配超链接文本
        8: By.TAG_NAME          - 按HTML标签名定位
        :param by_value:目标窗口独特元素的定位符
        :param mode: 定位模式（by_mapping），默认3
        :param timeout: 元素出现最大等待时间（默认10）
        :return: 没有跳转窗口（标签页）返回False,成功跳转目标窗口（标签页）返回True
        """
        # 记录最开始的窗口句柄
        original_window_handle = self.driver.current_window_handle
        # 遍历句柄并跳转标签页
        for window_handle in self.driver.window_handles:
            # 切换到新的标签页上
            self.driver.switch_to.window(window_handle)
            # 设置等待定位符，定位策略和时间，时间为10
            if self.wait_element_appear(by_value, mode, timeout):
                # 成功跳转指定的标签页
                return True
        # 跳回最开始的标签页
        self.driver.switch_to.window(original_window_handle)
        # 没有新的标签页
        return False

    def switch_win_ex(self, title: str, url: str, by_value: str, mode: int = 3) -> bool:
        """
        多重条件判定标签（窗口跳转成功），符合标题、url、存在特定元素才判定为跳转成功。
        须确保网页元素加载完成，因为判定条件是特定元素存在

        1: By.CSS_SELECTOR      - 性能好，写法灵活，推荐
        2: By.ID                - 性能最佳，元素唯一时首选
        3: By.XPATH             - 功能强大，可遍历DOM，但性能相对较差
        4: By.NAME              - 主要用于表单元素
        5: By.CLASS_NAME        - 按CSS类名定位
        6: By.LINK_TEXT         - 精确匹配超链接文本
        7: By.PARTIAL_LINK_TEXT - 部分匹配超链接文本
        8: By.TAG_NAME          - 按HTML标签名定位
        :param title: 目标窗口的标题
        :param url: 目标窗口的url
        :param by_value: 目标窗口独特元素的定位符
        :param mode: 定位模式（by_mapping），默认3
        :return: 没有跳转窗口（标签页）返回False,成功跳转目标窗口（标签页）返回True
        """
        # 记录最开始的窗口句柄
        original_window_handle = self.driver.current_window_handle
        # 遍历句柄并跳转标签页
        for window_handle in self.driver.window_handles:
            # 切换到新的标签页上
            self.driver.switch_to.window(window_handle)
            # 判定跳转网页是否符合给定标题、url、存在的元素
            if (self.driver.title == title and self.driver.current_url == url
                    and self.wait_element_appear(by_value, mode, 0)):
                # 成功跳转指定的标签页
                return True
        # 跳回最开始的标签页
        self.driver.switch_to.window(original_window_handle)
        # 没有新的标签页
        return False

