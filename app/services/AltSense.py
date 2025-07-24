import requests
from bs4 import BeautifulSoup

def fetch_all_img_tags(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  

        soup = BeautifulSoup(response.content, 'html.parser')
        img_tags = soup.find_all('img')

        
        return [str(tag) for tag in img_tags]

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []

