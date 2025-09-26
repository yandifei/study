from time import sleep

from selenium import webdriver  # 控制浏览器
from selenium.webdriver.chrome.service import  Service  # 用于设置一些配置信息
from selenium.webdriver.common.by import By

service = Service(r"C:\Program Files\Google\Chrome\Application\chromedriver-win64\chromedriver.exe")

# 传入浏览器驱动位置
driver = webdriver.Chrome(service=service)

driver.maximize_window()

driver.get("http://news.baidu.com")

# 元素定位
news_input = driver.find_element(By.ID,"ww")
news_input.send_keys("台风")


# 定位百度一下按钮，并且点击
search_button = driver.find_element(By.ID, "s_btn_wr")
search_button.click()

# 打开
sleep(5)











driver.quit()
