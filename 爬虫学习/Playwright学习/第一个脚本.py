# 在第一个脚本中，我们将导航到 https://playwright.dev/ 并在WebKit中截图：
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.webkit.launch(headless=False)
    page = browser.new_page()
    page.goto("https://playwright.dev/")
    page.screenshot(path="example.png")
    browser.close()