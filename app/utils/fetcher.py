from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import sys


def prettify_html(html_content):
    """
    Takes raw HTML content and returns it in a prettified (indented) format.

    Args:
        html_content (str): The raw HTML string.

    Returns:
        str: The prettified HTML string.
    """
    if html_content:
        soup = BeautifulSoup(html_content, "html.parser")
        return soup.prettify()
    return ""  # Return an empty string if content is empty or None


# Function to fetch HTML content using Selenium
def fetch_html_with_selenium(url):
    """
    Fetches the HTML content of a webpage using Selenium in headless mode.

    Args:
        url (str): The URL of the webpage to fetch.

    Returns:
        str: The HTML content of the webpage, or None if an error occurs.
    """
    options = Options()

    options.add_argument("--headless")

    options.add_argument("--no-sandbox")

    options.add_argument("--disable-dev-shm-usage")

    options.add_argument("--user-data-dir=/tmp/user-data")

    driver = None
    try:
        driver = webdriver.Chrome(options=options)

        driver.get(url)

        html = driver.page_source
        return html
    except Exception as e:
        print(f"Error fetching {url} with Selenium: {e}", file=sys.stderr)
        return None
    finally:
        if driver:
            driver.quit()



