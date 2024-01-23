import asyncio
from playwright.async_api import async_playwright, Playwright

async def run(playwright: Playwright):
    firefox = playwright.chromium
    browser = await firefox.launch(headless=False)
    page = await browser.new_page()
    await page.goto("https://www.drushim.co.il/jobs/subcat/307/")
    await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)
asyncio.run(main())


print("")
