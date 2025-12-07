from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://playwright.dev/")
    page.screenshot(path="example.png")
    browser.close()

"""打包指令
bash指令：
PLAYWRIGHT_BROWSERS_PATH=0 playwright install chromium
pyinstaller -F main.py

PowerShell指令：
$env:PLAYWRIGHT_BROWSERS_PATH="0"
playwright install chromium
pyinstaller -F main.py

Batch指令：
set PLAYWRIGHT_BROWSERS_PATH=0
playwright install chromium
pyinstaller -F main.py

将浏览器与可执行文件捆绑在一起会生成更大的二进制文件。建议仅捆绑您使用的浏览器。
"""