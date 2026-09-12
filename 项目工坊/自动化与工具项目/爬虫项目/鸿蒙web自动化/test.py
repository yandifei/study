"""目标：爬取数据
鸿蒙应用开发初级飞书链接：https://dvjmyvyohm7.feishu.cn/docx/QJa3dfmzmot3dvxusMZcyusGnDh
密码：5M9@3271
"""
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By

from core.driver_factory import DriverFactory   # 导入驱动工厂
from pages.腾科题库 import 腾科题库

df = DriverFactory("chromedriver.exe",
                   "./Google Chrome/chrome.exe",
                   "./Google Chrome Headless/chrome-headless-shell.exe"
                   )


driver = df.create_driver(False)

tk = 腾科题库(driver)
tk.get()

sleep(10)

driver.quit()

