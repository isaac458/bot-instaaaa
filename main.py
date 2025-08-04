import asyncio
from playwright.async_api import async_playwright
import os

GREET_TEXT = "ياهلا نورتنا @{}"
GREETS_FILE = "users_greeted.txt"

async def load_greeted():
    if not os.path.exists(GREETS_FILE):
        return set()
    return set(line.strip() for line in open(GREETS_FILE, encoding="utf8"))

async def save_greeted(users):
    with open(GREETS_FILE, "w", encoding="utf8") as f:
        for u in users:
            f.write(u + "\n")

async def run():
    greeted = await load_greeted()
    username = os.getenv("goojo_3amk")
    password = os.getenv("qwerrewq123321##")
    group_url = os.getenv("https://www.instagram.com/direct/t/24075104438837157/")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.instagram.com/accounts/login/")
        await page.fill("input[name='username']", username)
        await page.fill("input[name='password']", password)
        await page.click("button[type='submit']")
        await page.wait_for_navigation()

        await page.goto(group_url)
        print("✅ Group chat opened")

        while True:
            msgs = await page.query_selector_all("div[role='presentation'] div[dir='auto']")
            for msg in msgs[-10:]:
                text = await msg.inner_text()
                if text.startswith("@"):
                    user = text.split()[0][1:]
                    if user not in greeted:
                        await page.focus("textarea")
                        await page.fill("textarea", GREET_TEXT.format(user))
                        await page.press("textarea", "Enter")
                        greeted.add(user)
                        await save_greeted(greeted)
                        print(f"👋 Greeted {user}")
            await asyncio.sleep(5)

asyncio.run(run())
