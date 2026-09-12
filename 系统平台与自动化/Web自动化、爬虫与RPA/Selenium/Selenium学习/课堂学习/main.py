# from selenium import webdriver  # 控制浏览器
#
#
# driver = webdriver.Chrome()
#
# driver.get("http://selenium.dev")
#
# driver.quit()
#
# print("hello world")
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

print(f"ChromeDriver 文件的自动下载位置是：{driver.service.path}")

# 绑定网址
driver.get("https://www.jd.com/")

# 开始会有广告（不一定会有，初次访问或第一次账号登陆）
# 京东广告关闭按钮
guan_input = driver.find_element(By.XPATH,"""//*[@id="umc-equity-close-btn"]/div/svg""")

# 点击京东广告关闭按钮
guan_input.click()

# 京东输入定位
search_input = driver.find_element(By.XPATH,"""//*[@id="key"]""")

# 京东输入文本
search_input.send_keys("固态硬盘")

# 京豆搜索按钮

search_botton = driver.find_element(By.CSS_SELECTOR, """#search > div.search-m > div.form.include_jingyan.hotWords > button""")

# 点击京豆搜索按钮
search_input.send_keys()
# 点击第二次（第一次可能有广告弹出）
search_input.send_keys()



sleep(10000)

driver.quit()