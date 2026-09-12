from selenium import webdriver
from selenium.webdriver.common.by import By


def test_eight_components():
    # 启动驱动器
    driver = setup()
    # 拿到标签页的标题
    title = driver.title
    assert title == "Web form"  # 关键：断言（判断标题是否为"Web form"，不是则抛出异常）

    # 隐式等待(全局设置，它告诉 WebDriver 在尝试查找一个或多个元素时，如果立即没有找到，应该等待的最长时间。)
    driver.implicitly_wait(0.5)

    text_box = driver.find_element(by=By.NAME, value="my-text")
    submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

    text_box.send_keys("Selenium")
    submit_button.click()

    message = driver.find_element(by=By.ID, value="message")
    value = message.text
    assert value == "Received!"

    teardown(driver)

def setup():
    """
    启动驱动器
    :return:  driver对象
    """
    driver = webdriver.Chrome()
    driver.get("https://www.selenium.dev/selenium/web/web-form.html")
    return driver

def teardown(driver):
    """
    停止驱动器进程
    :param driver:
    :return:
    """
    driver.quit()
