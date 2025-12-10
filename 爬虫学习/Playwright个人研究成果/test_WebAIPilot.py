# from playwright.sync_api import sync_playwright
#
# # 启动playwright进程
# playwright = sync_playwright().start()
#
# # 启动浏览器
# browser = playwright.chromium.launch(headless=False)
#
# # 创建新界面，返回Page对象
# page = browser.new_page()
#
# # 标签页跳转到豆包网址
# page.goto("https://www.doubao.com/chat/")
#
# # 等待加载
# page.wait_for_timeout(1000)
#
# # 打印网页标题栏
# print(page.title())
#
# # 关闭浏览器
# browser.close()
#
# # 关闭playwright进程
# playwright.stop()


