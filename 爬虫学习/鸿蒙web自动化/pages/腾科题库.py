"""腾科题库.py

"""
from pywebauto import BaseActions
from selenium import webdriver


class 腾科题库(BaseActions):
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver

    def get(self):
        self.driver.get("https://dvjmyvyohm7.feishu.cn/docx/QJa3dfmzmot3dvxusMZcyusGnDh")
        element = self.wait_click("#mainContainer > div.app-main-container.flex.layout-row.explorer-v3.is-suite > div.app-main.main__content.layout-column.app-main-header-flexible > div.suite-body.flex.layout-column > div > div.styles__DescriptionWrapper-haagzD.hHEIVW > div > div.layout-row.password-required-container > div > input")
        element.send_keys("5M9@3271")
        # self.send_key_ex("#mainContainer > div.app-main-container.flex.layout-row.explorer-v3.is-suite > div.app-main.main__content.layout-column.app-main-header-flexible > div.suite-body.flex.layout-column > div > div.styles__DescriptionWrapper-haagzD.hHEIVW > div > div.layout-row.password-required-container > div > input",
        #                  1,
        #                  10,
        #                  "5M9@3271", )
