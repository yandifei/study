"""cookie_manager.py
cookie管理者封装
1. 检查cookie是否有效
2. 保存最新的cookie
3. 对当前网址进行cookie注入
4. 检查cookie是否注入成功
"""
# 官方库
import json
# 第三方库
from selenium import webdriver
from selenium.common import InvalidCookieDomainException

class CookieManager:
    def __init__(self, driver: webdriver.Chrome):
        """
        cookies管理封装，提供管理的方法，后续进阶自动cookies管理
        :param driver: 谷歌浏览器驱动对象
        """
        # 驱动
        self.driver: webdriver.Chrome= driver

    """==============================================cookies保存封装=============================================="""

    def save_cookies(self, path: str = "cookies.json") -> bool:
        """
        保存当前页面的cookies
        :param path: 文件保存路径或文件名
        :return: 注入失败、cookies文件为空或被错误修改返回False,注入成功返回True。
        无法保证cookies有效，仅保证cookies注入成功。注入错网址会导致注入失败
        """
        # 文件存在直接写入，文件不存在直接创建文件后写入
        with open(fr"{path}", "w", encoding="utf-8") as cookies_file:
            # 获取浏览器的cookies，传入cookies_file这个链接对象
            json.dump(self.driver.get_cookies(), cookies_file)
        return True

    def inject_cookies(self, path: str = "cookies.json", save_now_cookies: bool = False):
        """
        对当前网址注入cookies
        :param path: cookies保存路径
        :param save_now_cookies: 是否保存注入后的cookies
        :return: 成功True，否则False
        """
        try:
            with open(fr"{path}", "r", encoding="utf-8") as cookies_file:
                cookies_data = json.load(cookies_file)  # 返回的其实是一个列表
        except json.JSONDecodeError:
            print(f"{path}为空或被错误修改")
            return False

        try:
            # 读取cookies文件的所有cookies
            for cookie in cookies_data:
                # 对该网址注入cookie
                self.driver.add_cookie(cookie)
        except  InvalidCookieDomainException:    # 注入失败
            return False

        # 刷新网页（一般显示登陆成功）
        self.driver.refresh()
        if save_now_cookies:
            # 重新保存cookies，因为有时候UDP会用上，保持20分钟的链接
            self.save_cookies(path)
        return True