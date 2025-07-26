from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import sys
import asyncio

def prettify_html(html_content):
    if html_content:
        soup = BeautifulSoup(html_content, "html.parser")
        return soup.prettify()
    return ""

# Async wrapper for running sync Selenium code
async def fetch_html_with_selenium(url):
    loop = asyncio.get_event_loop()
    html = await loop.run_in_executor(None, _sync_fetch_html_with_selenium, url)
    return html

# The actual Selenium logic
def _sync_fetch_html_with_selenium(url):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        return driver.page_source
    except Exception as e:
        print(f"Error fetching {url} with Selenium: {e}", file=sys.stderr)
        return None
    finally:
        if driver:
            driver.quit()

