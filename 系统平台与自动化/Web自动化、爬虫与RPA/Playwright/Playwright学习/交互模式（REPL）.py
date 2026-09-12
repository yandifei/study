# 您可以启动交互式Python REPL：
from playwright.sync_api import sync_playwright
playwright = sync_playwright().start()
# 使用 playwright.chromium、playwright.firefox 或 playwright.webkit
# 向 launch() 传递 headless=False 以查看浏览器界面
browser = playwright.chromium.launch()
page = browser.new_page()
page.goto("https://playwright.dev/")
page.screenshot(path="example.png")
browser.close()
playwright.stop()

# 异步REPL（如asyncio REPL）：

# python -m asyncio

# from playwright.async_api import async_playwright
# playwright = await async_playwright().start()
# browser = await playwright.chromium.launch()
# page = await browser.new_page()
# await page.goto("https://playwright.dev/")
# await page.screenshot(path="example.png")
# await browser.close()
# await playwright.stop()