from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


# service = Service()
# service.path = r"C:\Users\yandifei\.cache\selenium\chromedriver\win64\140.0.7339.207\chromedriver.exe"

# 使用驱动实例开启会话
# driver = webdriver.Chrome(service = service)
driver = webdriver.Chrome()

# 导航 到一个网页.
driver.get("https://www.selenium.dev/selenium/web/web-form.html")

# 请求 浏览器信息
title = driver.title
print(title)

# 建立等待策略
driver.implicitly_wait(0.5)

# 发送命令 查找元素
text_box = driver.find_element(by=By.NAME, value="my-text")
submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

# 对于一个元素, 只有少数几个操作可以执行, 但您将经常使用它们.
# 共有4种，但是没有提到长按之类的，可能你在：https://www.selenium.dev/zh-cn/documentation/webdriver/actions_api/
text_box.send_keys("Selenium")  # 写入
submit_button.click()           # 点击

# 获取元素信息
message = driver.find_element(by=By.ID, value="message")
text = message.text

#  结束会话（这将结束驱动程序进程, 默认情况下, 该进程也会关闭浏览器. 无法向此驱动程序实例发送更多命令.）
driver.quit()

print(driver.service.path)
