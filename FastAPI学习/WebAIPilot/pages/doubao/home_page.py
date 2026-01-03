"""home_page.py.py
豆包主界面
"""
import re
from pathlib import Path
from typing import Sequence

from playwright.async_api import FilePayload, expect
from playwright.async_api import Page

from pages.base_page import BasePage
from utils import ConfigManager, info, debug


class HomePage(BasePage):
    """豆包主界面"""

    async def _async_init(self):
        """
        异步初始化豆包主页面
        :return: None
        """
        # 访问豆包对话网页
        await self.page.goto(self.cm.config_data["AI"]["doubao"]["chat_url"])
        # 等待界面加载完成
        await self.wait_for_load_state("domcontentloaded")
        # self.page.locator('img[src="https://lf-flow-web-cdn.doubao.com/obj/flow-doubao/samantha/logo-icon-white-bg.png"]').wait_for()
        self._is_initialized = True  # 更新自身状态

    def __init__(self, page, config_manager: ConfigManager):
        """初始化
        :param page:实例化的界面对象
        :param config_manager: 配置
        """
        super().__init__(page)
        # 界面对象
        self.page: Page = page
        # 生成原图url列表
        self.img_hook_list = []
        self.cm = config_manager


    async def ask(self, question: str, files: str | Path | FilePayload | Sequence[str | Path] | Sequence[FilePayload] | None = None):
        """
        在豆包主页上执行提问操作，支持文本和文件上传（异步版本）

        :param question: 要发送的提问文本内容
        :param files: 要上传的文件路径，支持以下格式：
                      - 单个字符串路径 (str)
                      - 单个 Path 对象 (Path)
                      - FilePayload 对象
                      - 文件路径列表 (list[str | Path])
                      - FilePayload 对象列表 (list[FilePayload])
                      - 为 None 时不上传文件
        :return: 元组 (text_answer: str, img_urls: list[str]) - 返回文本回答和图片URL列表
        """
        # 文件参数不是none，上传文件
        if files is not None:
            await self.page.locator('input[type="file"]').set_input_files(files)
            # 等待文件加载完成（无限等待直到完成）
            await self.page.get_by_test_id("chat_input_send_button").wait_for(timeout=0)
        # 等待输入框加载完成
        await self.page.get_by_placeholder("发消息或输入 / 选择技能").wait_for()
        # 输入内容
        await self.page.get_by_placeholder("发消息或输入 / 选择技能").fill(question)
        # 鼠标从输入框移动到发送按钮(悬浮2个控件会自动移动)
        await self.page.get_by_placeholder("发消息或输入 / 选择技能").hover()
        # await self.page.get_by_test_id("chat_input_send_button").hover()
        send_btn = self.page.get_by_test_id("chat_input_send_button")
        box = await send_btn.bounding_box()
        await self.page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=20)
        # 等待发送按钮可见且可点击
        await expect(self.page.get_by_test_id("chat_input_send_button")).to_be_visible()
        await expect(self.page.get_by_test_id("chat_input_send_button")).to_be_enabled()
        debug(f"问题输入完毕:{question}\n文件{files}")
        # 发送（click会被风控）
        await self.page.get_by_test_id("chat_input_send_button").press("Enter")
        # 在页面启动时挂载图片生成监听器(先清空列表)
        self.page.on("response", self.img_hook); self.img_hook_list.clear()
        # 等待回复完成(时间是无限等待)
        await self.page.get_by_test_id("chat_input_local_break_button").wait_for(state="hidden", timeout=0)
        await self.page.get_by_test_id("asr_btn").wait_for(state="visible", timeout=0)
        debug("豆包回答生成完毕")
        # 等待复制标签出现
        await self.page.get_by_test_id("message_action_copy").wait_for()
        # 点击复制标签
        await self.page.get_by_test_id("message_action_copy").click()
        # 同步获取捕获到的变量，evaluate 会等待并返回结果
        text_answer = await self.page.evaluate("window.tempCopyBuffer")
        debug(f"最终拿到的文本回答: {text_answer}")
        debug(f"原图生成链接：{self.img_hook_list}")
        return text_answer, self.img_hook_list.copy()


    async def get_last_answer(self):
        """
        获取最后对话中豆包回复的内容（异步版本）

        :return: 元组 (text_answer: str, img_urls: list[str]) - 返回文本回答和图片URL列表
        """
        # 等待复制标签出现
        await self.page.get_by_test_id("message_action_copy").wait_for()
        # 点击复制标签
        await self.page.get_by_test_id("message_action_copy").click()
        # 同步获取捕获到的变量，evaluate 会等待并返回结果
        text_answer = await self.page.evaluate("window.tempCopyBuffer")
        # 放置图片钩子
        self.page.on("response", self.img_all_hook)
        # 清空图片列表
        self.img_hook_list.clear()
        # 刷新网页（启动钩子）
        await self.page.reload()
        info(f"最终拿到的文本回答: {text_answer}")
        info(f"所有生成的图像链接：{self.img_hook_list}")
        return text_answer, self.img_hook_list.copy()

    async def get_all_conversation_tags(self):
        """
        获取所有会话标签（异步版本）

        :return: 所有会话标签
        """
        return await self.page.locator(".message_content").all()

    async def get_imgs_urls(self):
        """
        获取当前对话中所有图片没有水印下载链接（异步版本）

        :return: 所有图片的没有水印下载链接
        """
        # 放置图片钩子
        self.page.on("response", self.img_all_hook)
        # 刷新网页（启动钩子）
        await self.page.reload()
        return self.img_hook_list.copy()

    async def img_hook(self, response):
        """从豆包对话中获取图片的没有水印下载链接（异步版本）

        :param response: 回调参数
        :return:
        """
        # 不看完整 URL，只看关键字
        if "https://www.doubao.com/chat/completion?aid=" in response.url:
            # 正则提取所有 image_ori_raw 下的 url 内容
            matches = re.findall(r'"image_ori_raw":\{"url":"(.*?)"', await response.text())
            # 遍历所有匹配项
            for raw_url in matches:
                # 判定条件：过滤掉以反斜杠 \ 结尾的"中间态"或"假"URL
                if raw_url.endswith('\\'):
                    continue
                # Unicode 解码并存储这个真实的无水印url
                self.img_hook_list.append(raw_url.encode().decode('unicode_escape'))

    async def img_all_hook(self, response):
        """从豆包对话中获取所有图片的没有水印下载链接（异步版本）

        :param response: 回调参数
        :return:
        """
        # 不看完整 URL，只看关键字
        if "https://www.doubao.com/im/chain/single?version_code=" in response.url:
            # 正则提取所有 image_ori_raw 下的 url 内容
            matches = re.findall(r'"image_ori_raw":\{"url":"(.*?)"', await response.text())
            # 遍历所有匹配项
            for raw_url in matches:
                # 判定条件：过滤掉以反斜杠 \ 结尾的"中间态"或"假"URL
                if raw_url.endswith('\\'):
                    continue
                # Unicode 解码并存储这个真实的无水印url
                self.img_hook_list.append(raw_url.encode().decode('unicode_escape'))

    """web对话相关"""
    async def create_conversation(self):
        """创建新对话（异步版本）

        :return: None
        """
        await self.page.get_by_test_id("create_conversation_button").click()

    async def get_conversation_count(self):
        """获取当前会话数量（异步版本）

        :return: 当前会话数量
        """
        return await self.page.get_by_test_id('chat_list_thread_item').count()

    async def get_conversation_title_list(self):
        """获取当前会话列表（标题存储）（异步版本）

        :return: 当前会话列表(标题存储)
        """
        conversation_list = []
        # 遍历所有会话
        for item in await self.page.get_by_test_id('chat_list_item_title').all():
            # 获取标题并添加到列表中
            conversation_list.append(await item.text_content())
        return conversation_list

    async def switch_conversation(self, index: int | str = 0):
        """切换会话（异步版本）

        :param index: 会话索引，可以是下标、会话的标题
        :return: 成功切换返回True，否则返回False
        """
        # 下标索引
        if isinstance(index, int):
            try:
                # 点击这个对话
                await self.page.get_by_test_id('chat_list_thread_item').nth(index).click()
            except IndexError:
                return False
        # 标题索引
        for item in await self.page.get_by_test_id('chat_list_item_title').all():
            # 标题对上
            if await item.text_content() == index:
                # 点击这个对话
                await item.click()
                break
        else:
            return False
        return True

    async def del_conversation(self, index: int | str = 0):
        """删除会话（异步版本）

        :param index: 会话索引，可以是下标、会话的标题
        :return: 删除成功返回True，否则返回False
        """
        # 下标索引
        if isinstance(index, int):
            try:
                # 点击更多按钮
                item = self.page.get_by_test_id('chat_list_thread_item').nth(index)
                await item.locator(".size-14.bg-transparent").click()
                # 点击删除按钮
                await self.page.get_by_test_id('chat_item_menu_remove_icon').click()
                # 点击确认删除按钮
                await self.page.get_by_label("confirm").click()
            except IndexError:
                return False
        # 标题索引
        for item in await self.page.get_by_test_id('chat_list_item_title').all():
            if await item.text_content() == index:
                # 点击更多按钮
                await item.locator(".size-14.bg-transparent").click()
                # 点击删除按钮
                await self.page.get_by_test_id('chat_item_menu_remove_icon').click()
                # 点击确认删除按钮
                await self.page.get_by_label("confirm").click()
                break
        else:
            return False
        return True

    async def deep_thinking_mode(self, switch: bool = True) -> None:
        """
        控制深度思考模式的开关

        :param switch: 布尔值，True为开启深度思考模式，False为关闭深度思考模式，默认为True
        :return: None
        """
        if switch:
            # 判断是否处于关闭
            if await self.page.get_by_role("button", name="深度思考").get_attribute("data-checked") == "false":
                await self.page.get_by_role("button", name="深度思考").click()
        else:
            # 判断是否处于开启
            if await self.page.get_by_role("button", name="深度思考").get_attribute("data-checked") == "true":
                await self.page.get_by_role("button", name="深度思考").click()

    async def image_generation_mode(self, switch: bool = True) -> None:
        """
        控制图片生成模式的开关

        :param switch: 布尔值，True为开启图片生成模式，False为关闭图片生成模式，默认为True
        :return: None
        """
        if switch:
            # 判断是否处于关闭
            if await self.page.get_by_role("button", name="图像生成").get_attribute("data-checked") == "false":
                await self.page.get_by_role("button", name="图像生成").click()
        else:
            # 判断是否处于开启
            if await self.page.get_by_role("button", name="图像生成").get_attribute("data-checked") == "true":
                await self.page.get_by_role("button", name="图像生成").click()

    async def help_me_write_mode(self, switch: bool = True) -> None:
        """
        控制帮我写作模式的开关

        :param switch: 布尔值，True为开启帮我写作模式，False为关闭帮我写作模式，默认为True
        :return: None
        """
        if switch:
            # 判断是否处于关闭
            if await self.page.get_by_role("button", name="帮我写作").get_attribute("data-checked") == "false":
                await self.page.get_by_role("button", name="帮我写作").click()
        else:
            # 判断是否处于开启
            if await self.page.get_by_role("button", name="帮我写作").get_attribute("data-checked") == "true":
                await self.page.get_by_role("button", name="帮我写作").click()

    async def video_generation_mode(self, switch: bool = True) -> None:
        """
        控制视频生成模式的开关

        :param switch: 布尔值，True为开启视频生成模式，False为关闭视频生成模式，默认为True
        :return: None
        """
        if switch:
            # 判断是否处于关闭
            if await self.page.get_by_role("button", name="视频生成").get_attribute("data-checked") == "false":
                await self.page.get_by_role("button", name="视频生成").click()
        else:
            # 判断是否处于开启
            if await self.page.get_by_role("button", name="视频生成").get_attribute("data-checked") == "true":
                await self.page.get_by_role("button", name="视频生成").click()

    async def translation_mode(self, switch: bool = True) -> None:
        """
        控制翻译模式的开关

        :param switch: 布尔值，True为开启翻译模式，False为关闭翻译模式，默认为True
        :return: None
        """
        if switch:
            # 判断是否处于关闭
            if await self.page.get_by_role("button", name="翻译").get_attribute("data-checked") == "false":
                await self.page.get_by_role("button", name="翻译").click()
        else:
            # 判断是否处于开启
            if await self.page.get_by_role("button", name="翻译").get_attribute("data-checked") == "true":
                await self.page.get_by_role("button", name="翻译").click()


    # 还有更多模型，这个就不搞了，太多了
    pass