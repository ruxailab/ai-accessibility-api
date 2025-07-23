import requests
from bs4 import BeautifulSoup

def scrape_img_tags(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')

    return [str(tag) for tag in img_tags]

if __name__ == "__main__":
    input_url = input("Enter website URL: ").strip()
    img_elements = scrape_img_tags(input_url)

    print(f"\nFound {len(img_elements)} <img> tags:\n")
    for tag in img_elements:
        print(tag)
