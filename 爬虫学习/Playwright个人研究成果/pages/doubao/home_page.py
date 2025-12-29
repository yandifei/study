"""home_page.py.py
豆包主界面
"""
import re
from pathlib import Path
from time import sleep
from typing import Sequence

from playwright.sync_api import FilePayload, expect
from playwright.sync_api import Page

from pages.base_page import BasePage
from utils import ConfigManager, info


class HomePage(BasePage):
    """豆包主界面"""

    def __init__(self, page, config_manager: ConfigManager):
        """初始化
        :param page:实例化的界面对象
        :param config_manager: 配置
        """
        super().__init__(page)
        # 界面对象
        self.page: Page = page
        # 访问豆包对话网页
        self.page.goto(config_manager.config_data["AI"]["doubao"]["chat_url"])
        # 等待界面加载完成
        self.wait_for_load_state("domcontentloaded")
        # self.page.locator('img[src="https://lf-flow-web-cdn.doubao.com/obj/flow-doubao/samantha/logo-icon-white-bg.png"]').wait_for()

    def ask(self, text: str, files: str | Path | FilePayload | Sequence[str | Path] | Sequence[FilePayload] | None = None):
        """
        在豆包主页上执行提问操作，支持文本和文件上传

        :param text: 要发送的提问文本内容
        :param files: 要上传的文件路径，支持以下格式：
                      - 单个字符串路径 (str)
                      - 单个 Path 对象 (Path)
                      - 文件路径列表 (list[str | Path])
                      - 为 None 时不上传文件
        :return: None
        """
        self.page.add_init_script("""
        // 初始化全局变量
        window.tempCopyBuffer = ""; 
        // 改变js行为
        document.addEventListener('copy', (event) => {
            // 阻止原来的startMonitoring 运行
            event.stopImmediatePropagation();
            // 拦截行为：阻止事件冒泡和默认行为
            event.preventDefault();
            // 同步获取：直接从当前选区抓取文本
            const selection = document.getSelection().toString();
            // 存储到变量
            window.tempCopyBuffer = selection;
        }, true);""")
        # 文件参数不是none，上传文件
        if files is not None:
            self.page.locator('input[type="file"]').set_input_files(files)
            # 等待文件加载完成（无限等待直到完成）
            self.page.get_by_test_id("chat_input_send_button").wait_for(timeout=0)
        # 等待输入框加载完成
        self.page.get_by_placeholder("发消息或输入 / 选择技能").wait_for()
        # 输入内容
        self.page.get_by_placeholder("发消息或输入 / 选择技能").fill(text)
        # 等待发送按钮可见且可点击
        expect(self.page.get_by_test_id("chat_input_send_button")).to_be_visible()
        expect(self.page.get_by_test_id("chat_input_send_button")).to_be_enabled()
        info("问题构造完毕")
        # 发送（click会被风控）
        self.page.get_by_test_id("chat_input_send_button").press("Enter")
        # 记录当前AI的对话数量
        count = self.page.locator('.flex-row.flex.w-full.justify-end').count()
        info("点击发送")
        # 不可靠的等待回复加载完成（完成后，发送图标会变成语音图标）
        self.page.get_by_test_id("asr_btn").wait_for(timeout=0)
        # AI回复数增加1才算是回复完毕
        while self.page.locator('.flex-row.flex.w-full.justify-end').count() == count:
            self.page.wait_for_timeout(1000)


    def get_answer(self):
        """
        获取豆包回复内容

        :return: 豆包回复内容
        """

        # # 等待回复完毕出现复制标签
        # self.page.locator(".message_content").last.get_by_test_id("message_action_copy").wait_for()
        # self.page.wait_for_timeout(3000)
        info("回复完毕")
        # # 检查回复是否可见
        # if not self.page.locator(".message_content").last.is_visible():
        #     info("没有对话内容")
        #     return False
        # 获取图片下载链接(传递最后1个会话的html)
        print(self.get_img_scr_list(self.page.locator('.flex-row.flex.w-full.justify-end').last.inner_html()))
#         # 获取回复内容
#         self.page.add_init_script("""
# // 初始化全局变量
# window.tempCopyBuffer = "";
# // 改变js行为
# document.addEventListener('copy', (event) => {
#     // 阻止原来的startMonitoring 运行
#     event.stopImmediatePropagation();
#     // 拦截行为：阻止事件冒泡和默认行为
#     event.preventDefault();
#     // 同步获取：直接从当前选区抓取文本
#     const selection = document.getSelection().toString();
#     // 存储到变量
#     window.tempCopyBuffer = selection;
# }, true);""")
        # # 如果你不想点按钮，直接触发事件即可
        # self.page.evaluate("document.dispatchEvent(new ClipboardEvent('copy'))")
        # 等待复制标签出现
        self.page.get_by_test_id("message_action_copy").wait_for()
        # 点击复制标签
        self.page.get_by_test_id("message_action_copy").click()
        # 等待复制完毕
        self.page.wait_for_timeout(3000)
        # 4. 同步获取捕获到的变量
        # evaluate 会等待并返回结果
        answer = self.page.evaluate("window.tempCopyBuffer")
        print(f"最终拿到的回答: {answer}")
        return answer

    def get_img_scr_list(self, html: str):
        """从指定对话html中获取图片的下载链接

        :param html:
        :return:
        """
        # 获取html回复的链接内容
        urls = re.findall(r'https://[^\s"\'<>]+?byteimg\.com[^\s"\'<>]+', html)
        # 清洗链接：HTML 反转义 + 去重
        image_links = []
        for url in urls:
            # 处理 HTML 转义：把 &amp; 替换回 & (这是下载成功的核心)
            # 处理 srcset 格式：截取空格前的内容（防止带上 1x, 2x 标识）
            clean_url = url.replace('&amp;', '&').split(' ')[0]
            if clean_url not in image_links:
                image_links.append(clean_url)
        return image_links


    def get_all_conversation_tags(self):
        """
        获取所有会话标签

        :return: 所有会话标签
        """
        return self.page.locator(".message_content").all()


"""
flex-row flex w-full 我的问题标签
flex-row flex w-full justify-end AI的回答标签


# 遍历文件路径列表并发送
# for file_path in file_path_list:
#     # 点击按钮会触发 file chooser
#     with self.page.expect_file_chooser() as fc_info:
#         # 定位文件输入框
#         self.page.get_by_test_id("upload_file_button").click()
#         # 文件选择
#         file_chooser = fc_info.value
#         self.page.wait_for_timeout(3000)
#         # 上传单个文件
#         file_chooser.set_files(file_path)
#         self.page.wait_for_timeout(3000)
#         # 等待文件上传完毕
#         self.page.get_by_test_id("chat_input_send_button").is_enabled()
#         self.page.wait_for_timeout(3000)


document.addEventListener('copy', (event) => {
    // 获取用户当前选中的文本
    const selection = document.getSelection().toString();
    console.log('用户复制了内容：', selection);
    event.preventDefault(); // 阻止默认行为以应用你的修改
});



document.addEventListener('copy', () => {
  // 延迟一瞬确保剪贴板已更新，或者直接获取当前选区内容
  setTimeout(async () => {
    const text = await navigator.clipboard.readText();
    console.log(text);
  }, 10);
}, true);

// 改进版(没有数据输出)
const answer
document.addEventListener('copy', () => {
    const text = navigator.clipboard.readText();
    return text;
});


// 找到所有带有埋点定义的元素（没有html）
const telemetryElements = document.querySelectorAll('[data-copy-telemetry]');
telemetryElements.forEach(el => {
    console.log('目标元素:', el);
    console.log('对应的埋点值:', el.getAttribute('data-copy-telemetry'));
    // 你可以直接读取这些元素的 innerText，这就是它想保护或监控的内容
    console.log('元素内容:', el.innerText);
});
"""