import requests
from bs4 import BeautifulSoup

def scrape_anchor_tags(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    anchor_tags = soup.find_all('a')

    return [str(tag) for tag in anchor_tags]

if __name__ == "__main__":
    input_url = input("Enter website URL: ").strip()
    anchor_elements = scrape_anchor_tags(input_url)

    print(f"\nFound {len(anchor_elements)} <a> tags:\n")
    for tag in anchor_elements:
        print(tag)
