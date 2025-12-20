"""
Playwright 工厂 & 管理封装
"""
# 系统库
from __future__ import annotations # 解决3.7 - 3.9的py版本传递自身抛出错误问题

import threading
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, Generator, Literal, Union, Sequence

from playwright.async_api import ProxySettings
# 第三方库
from playwright.sync_api import sync_playwright, Playwright, Browser, BrowserContext, Page
# 自己的模块
from utils import warning
from utils.playwright_factory.launch_options import LaunchOptions
from utils.playwright_factory.context_options import ContextOptions



class PlaywrightFactory:
    """
    Playwright工厂
    管理sync_playwright()的生命周期
    生产browser和context
    """
    # 存储单例实例的类变量
    _instance = None
    # 类级锁，确保多线程环境下的线程安全
    _lock = threading.Lock()
    # 启动配置
    launch_options: LaunchOptions
    # 上下文配置
    context_options: ContextOptions

    def __new__(cls, launch_options: LaunchOptions, context_options: ContextOptions):
        """确保创建为单例:线程安全双重检查锁定 (DCL)"""
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

    def __init__(self, launch_options: LaunchOptions = LaunchOptions(), context_options: ContextOptions = ContextOptions()):
        # 确保配置只加载一次(Pythonic写法)
        if not hasattr(self, '_initialized'):
            # 设置被初始化的标志位
            self._initialized = True
            # playwright启动状态
            self.__playwright_flag = False
            #
            self.launch_options = launch_options
            self.context_options = context_options

            self.playwright = sync_playwright().start()
            browser = self.playwright.chromium.launch(**launch_options.to_dict())
            context = browser.new_context(**context_options.to_dict())
            page1 = context.new_page()
            page2 = context.new_page()
            page3 = context.new_page()
            page4 = context.new_page()
            context.close()
            browser.close()
            self.playwright.stop()



    def get_page(self, context: BrowserContext):
        """

        :param context:
        :return:
        """

    def get_context(self, browser: Browser):
        """

        :param browser:
        :return:
        """

    def get_browser(self, browser_type: Literal['chromium', 'firefox', 'webkit']):
        """获得1个浏览器

        :param browser_type: 浏览器类型（'chromium', 'firefox', 'webkit'）
        :return:
        """
        return self.playwright.chromium.launch(**launch_options.to_dict())

    def __exit__(self, exc_type, exc_val, exc_tb):


        # # 完整传递参数给父类（非继承没有这个方法）
        # return super().__exit__(exc_type, exc_val, exc_tb)
