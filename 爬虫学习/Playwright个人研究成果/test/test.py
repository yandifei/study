# import asyncio
# from playwright.async_api import async_playwright
# from playwright_stealth import Stealth
#
#
# async def main():
#     # This is the recommended usage. All pages created will have stealth applied:
#     async with Stealth().use_async(async_playwright()) as p:
#         browser = await p.chromium.launch()
#         page = await browser.new_page()
#
#         webdriver_status = await page.evaluate("navigator.webdriver")
#         print("from new_page: ", webdriver_status)
#
#         different_context = await browser.new_context()
#         page_from_different_context = await different_context.new_page()
#
#         different_context_status = await page_from_different_context.evaluate("navigator.webdriver")
#         print("from new_context: ", different_context_status)
#
#
# asyncio.run(main())
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

playwright = sync_playwright().start()

browser = playwright.chromium.launch(headless=True)
ctx = browser.new_context()
stealth = Stealth()
stealth.apply_stealth_sync(ctx)


playwright.stop()
