"""home_page.py
deepseek主界面
"""
from pathlib import Path
from typing import Sequence

from playwright.async_api import FilePayload, expect
from playwright.async_api import Page

from pages.base_page import BasePage
from utils import ConfigManager, info, debug

class HomePage(BasePage):
    """deepseek主界面"""

    async def _async_init(self):
        """
        异步初始化deepseek主页面
        :return: None
        """
        # 访问deepseek对话网页
        await self.page.goto(self.cm.config_data["AI"]["deepseek"]["chat_url"])
        self._is_initialized = True  # 更新自身状态

    def __init__(self, page, config_manager: ConfigManager):
        """初始化
        :param page:实例化的界面对象
        :param config_manager: 配置
        """
        super().__init__(page)
        # 界面对象
        self.page: Page = page
        self.cm = config_manager

    """对话操作"""
    async def ask(self, question: str, files: str | Path | FilePayload | Sequence[str | Path] | Sequence[FilePayload] | None = None):
        """
        在主页上执行提问操作，支持文本和文件上传（异步版本）

        :param question: 要发送的提问文本内容
        :param files: 要上传的文件路径，支持以下格式：
                      - 单个字符串路径 (str)
                      - 单个 Path 对象 (Path)
                      - FilePayload 对象
                      - 文件路径列表 (list[str | Path])
                      - FilePayload 对象列表 (list[FilePayload])
                      - 为 None 时不上传文件
        :return: text_answer: str - 返回文本回答
        """
        # 文件参数不是none，上传文件
        if files is not None:
            await self.page.locator('input[type="file"]').set_input_files(files)
            # 等待文件加载完成（无限等待直到完成）
            await expect(self.page.get_by_role("button")).to_have_attribute("aria-disabled", "false", timeout=0)
        # 等待输入框加载完成
        await self.page.locator('input[type="file"]').wait_for(state="hidden")
        # 输入内容
        await self.page.get_by_role("textbox", name="给 DeepSeek 发送消息 ").fill(question)
        # await expect(self.page.get_by_role("button").nth(4)).to_have_attribute("aria-disabled", "false", timeout=0)
        # 鼠标从输入框移动到发送按钮(悬浮2个控件会自动移动)
        await self.page.locator('div[style="width: fit-content;"]').hover()
        send_button = self.page.locator('div[style="width: fit-content;"]')
        box = await send_button.bounding_box()
        await self.page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=20)
        # 等待发送按钮可见且可点击
        await send_button.wait_for(state="visible")
        debug(f"问题输入完毕:{question}\n文件{files}")
        # 发送
        await send_button.click()
        # 等待回复完成(时间是无限等待)
        await expect(self.page.locator('div[style="width: fit-content;"]').get_by_role("button")).to_have_attribute("aria-disabled", "true", timeout=0)
        debug("deepseek回答生成完毕")
        # 点击复制标签（最后1个对话的第一个控件）
        await self.page.locator('div[style*="--assistant-last-margin-bottom: 32px;"]').last.locator('div[style="align-items: center; gap: 10px;"]').last.locator('div[role="button"]').first.click()
        # 同步获取捕获到的变量，evaluate 会等待并返回结果
        text_answer = await self.page.evaluate("window.tempCopyBuffer")
        debug(f"最终拿到的文本回答: {text_answer}")
        return text_answer

    async def get_last_answer(self):
        """
        获取最后对话中deepseek回复的内容（异步版本）

        :return: text_answer: str 返回文本回答
        """
        # 等待复制标签出现
        await self.page.locator('div[style*="--assistant-last-margin-bottom: 32px;"]').last.locator('div[style="align-items: center; gap: 10px;"]').last.locator('div[role="button"]').first.wait_for()
        # 点击复制标签
        await self.page.locator('div[style*="--assistant-last-margin-bottom: 32px;"]').last.locator('div[style="align-items: center; gap: 10px;"]').last.locator('div[role="button"]').first.click()
        # 同步获取捕获到的变量，evaluate 会等待并返回结果
        text_answer = await self.page.evaluate("window.tempCopyBuffer")
        debug(f"最后对话中deepseek回复的内容: {text_answer}")
        return text_answer

    async def get_all_conversation_turn (self):
        """
        获取所有对话历史（异步版本）

        :return: 所有对话历史的控件
        """
        return await self.page.locator('div[style="--panel-width: 0px;"]').all()

    """会话管理方法"""
    async def create_conversation(self):
        """创建新对话（异步版本）

        :return: None
        """
        # 经过了web的测试
        await self.page.locator("span").filter(has_text="开启新对话").click()

    async def del_conversation(self, identifier: int | str = 0):
        """删除会话（异步版本）

        :param identifier: 会话标识，可以是下标、会话的标题
        :return: 删除成功返回True，否则返回False
        """
        try:
            # 等待列表加载完成，不然.all()无效
            await self.page.wait_for_selector('div[class*="ds-scroll-area"] a[href^="/a/chat/s/"]', timeout=1000)
        except TimeoutError:
            return False
        # role="button"
        # 下标索引(不用担心下标移除，因为上面等待列表加载已经处理了)
        if isinstance(identifier, int):
            # 获取对应索引的会话项
            item = self.page.locator('div[class*="ds-scroll-area"] a[href^="/a/chat/s/"]').nth(identifier)
            # 悬浮（避免检测后又改）
            await item.hover()
            # 点击更多按钮（三个点）
            await item.get_by_role("button").click()
            # 点击删除按钮
            await self.page.locator('div.ds-dropdown-menu-option', has_text="删除").click()
            # 点击确认删除按钮
            await self.page.get_by_role("button", name="删除").click()
            return True
        # 标题索引
        for item in await self.page.locator('div[class*="ds-scroll-area"] a[href^="/a/chat/s/"]').all():
            if await item.inner_text() == identifier:
                # 悬浮（避免web检测后又改进）
                await item.hover()
                # 点击更多按钮（三个点）
                await item.get_by_role("button").click()
                # 点击删除按钮
                await self.page.locator('div.ds-dropdown-menu-option', has_text="删除").click()
                # 点击确认删除按钮
                await self.page.get_by_role("button", name="删除").click()
                break
        else:
            return False
        return True

    async def switch_conversation(self, identifier: int | str = 0):
        """切换会话（异步版本）

        :param identifier: 会话索引，可以是下标、会话的标题
        :return: 成功切换返回True，否则返回False
        """
        try:
            # 等待列表加载完成，不然.all()无效
            await self.page.wait_for_selector('div[class*="ds-scroll-area"] a[href^="/a/chat/s/"]', timeout=1000)
        except TimeoutError:
            return False
        # 下标索引(不用担心下标移除，因为上面等待列表加载已经处理了)
        if isinstance(identifier, int):
            if identifier > await self.page.locator('div[class*="ds-scroll-area"] a[href^="/a/chat/s/"]').count():
                return False
            # 点击这个对话
            await self.page.locator('div[class*="ds-scroll-area"] a[href^="/a/chat/s/"]').nth(identifier).click()
        else:
            # 标题索引
            for item in await self.page.locator('div[class*="ds-scroll-area"] a[href^="/a/chat/s/"]').all():
                # 标题对上
                if await item.inner_text() == identifier:
                    # 点击这个对话
                    await item.click()
                    break
            else:
                return False
        return True

    async def get_conversation_count(self):
        """获取当前会话数量（异步版本）

        :return: 当前会话数量
        """
        try:
            # 等待列表加载完成，不然.all()无效
            await self.page.wait_for_selector('div[class*="ds-scroll-area"] a[href^="/a/chat/s/"]', timeout=1000)
        except TimeoutError:
            pass
        return await self.page.locator('div[class*="ds-scroll-area"] a[href^="/a/chat/s/"]').count()

    async def get_conversation_title_list(self):
        """获取当前会话列表（标题存储）（异步版本）

        :return: 当前会话列表(标题存储)
        """
        conversation_list = []
        try:
            # 等待列表加载完成，不然.all()无效
            await self.page.wait_for_selector('div[class*="ds-scroll-area"] a[href^="/a/chat/s/"]', timeout=1000)
        except TimeoutError:
            pass
        # 遍历所有会话
        for item in await self.page.locator('div[class*="ds-scroll-area"] a[href^="/a/chat/s/"]').all():
            # 获取标题并添加到列表中
            conversation_list.append(await item.inner_text())
        return conversation_list

    """对话模式控制"""
    async def deep_thinking_mode(self, switch: bool = True) -> None:
        """
        控制深度思考模式的开关

        :param switch: 布尔值，True为开启深度思考模式，False为关闭深度思考模式，默认为True
        :return: None
        """
        if switch:
            # 判断是否处于关闭
            if not await self.page.locator("div[role='button'].ds-toggle-button--selected",has_text="深度思考").is_visible():
                await self.page.get_by_role("button", name="深度思考").click()
        else:
            # 判断是否处于开启
            if await self.page.locator("div[role='button'].ds-toggle-button--selected",has_text="深度思考").is_visible():
                await self.page.get_by_role("button", name="深度思考").click()

    async def network_mode(self, switch: bool = True) -> None:
        """
        控制联网模式的开关

        :param switch: 布尔值，True为开启深度思考模式，False为关闭深度思考模式，默认为True
        :return: None
        """
        if switch:
            # 判断是否处于关闭
            if not await self.page.locator("div[role='button'].ds-toggle-button--selected",has_text="联网搜索").is_visible():
                await self.page.get_by_role("button", name="联网搜索").click()
        else:
            # 判断是否处于开启
            if await self.page.locator("div[role='button'].ds-toggle-button--selected",has_text="联网搜索").is_visible():
                await self.page.get_by_role("button", name="联网搜索").click()






    # async def image_generation_mode(self, switch: bool = True) -> None:
    #     """
    #     控制图片生成模式的开关
    #
    #     :param switch: 布尔值，True为开启图片生成模式，False为关闭图片生成模式，默认为True
    #     :return: None
    #     """
    #     if switch:
    #         # 判断是否处于关闭
    #         if await self.page.get_by_role("button", name="图像生成").get_attribute("data-checked") == "false":
    #             await self.page.get_by_role("button", name="图像生成").click()
    #     else:
    #         # 判断是否处于开启
    #         if await self.page.get_by_role("button", name="图像生成").get_attribute("data-checked") == "true":
    #             await self.page.get_by_role("button", name="图像生成").click()
    #
    # async def help_me_write_mode(self, switch: bool = True) -> None:
    #     """
    #     控制帮我写作模式的开关
    #
    #     :param switch: 布尔值，True为开启帮我写作模式，False为关闭帮我写作模式，默认为True
    #     :return: None
    #     """
    #     if switch:
    #         # 判断是否处于关闭
    #         if await self.page.get_by_role("button", name="帮我写作").get_attribute("data-checked") == "false":
    #             await self.page.get_by_role("button", name="帮我写作").click()
    #     else:
    #         # 判断是否处于开启
    #         if await self.page.get_by_role("button", name="帮我写作").get_attribute("data-checked") == "true":
    #             await self.page.get_by_role("button", name="帮我写作").click()
    #
    # async def video_generation_mode(self, switch: bool = True) -> None:
    #     """
    #     控制视频生成模式的开关
    #
    #     :param switch: 布尔值，True为开启视频生成模式，False为关闭视频生成模式，默认为True
    #     :return: None
    #     """
    #     if switch:
    #         # 判断是否处于关闭
    #         if await self.page.get_by_role("button", name="视频生成").get_attribute("data-checked") == "false":
    #             await self.page.get_by_role("button", name="视频生成").click()
    #     else:
    #         # 判断是否处于开启
    #         if await self.page.get_by_role("button", name="视频生成").get_attribute("data-checked") == "true":
    #             await self.page.get_by_role("button", name="视频生成").click()
    #
    # async def translation_mode(self, switch: bool = True) -> None:
    #     """
    #     控制翻译模式的开关
    #
    #     :param switch: 布尔值，True为开启翻译模式，False为关闭翻译模式，默认为True
    #     :return: None
    #     """
    #     if switch:
    #         # 判断是否处于关闭
    #         if await self.page.get_by_role("button", name="翻译").get_attribute("data-checked") == "false":
    #             await self.page.get_by_role("button", name="翻译").click()
    #     else:
    #         # 判断是否处于开启
    #         if await self.page.get_by_role("button", name="翻译").get_attribute("data-checked") == "true":
    #             await self.page.get_by_role("button", name="翻译").click()

    # 还有更多模型，这个就不搞了，太多了
    pass