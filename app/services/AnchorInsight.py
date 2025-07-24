import requests
from bs4 import BeautifulSoup

def fetch_all_anchor_tags(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors

        soup = BeautifulSoup(response.content, 'html.parser')
        a_tags = soup.find_all('a')

        # Return the full <a> tag strings with all attributes
        return [str(tag) for tag in a_tags]

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []
