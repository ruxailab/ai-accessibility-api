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
    
import requests
import os

def download_image(img_tags, base_url, save_dir='.'):
    """
    Downloads images from a list of img tags.

    Args:
        img_tags (list): A list of BeautifulSoup img tags.
        base_url (str): The base URL of the website.
        save_dir (str): The directory to save the downloaded images.
    """
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for img_tag in img_tags:
        img_url = img_tag.get('src')
        if img_url:
            # Handle relative URLs
            if not img_url.startswith('http'):
                img_url = base_url + img_url

            try:
                response = requests.get(img_url, stream=True)
                response.raise_for_status()

                # Get the filename from the URL
                filename = os.path.join(save_dir, os.path.basename(img_url))

                # Save the image
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                print(f"Downloaded {filename}")

            except requests.exceptions.RequestException as e:
                print(f"Error downloading {img_url}: {e}")

# Example usage:
base_url = "https://saltywebsite.vercel.app"
img_tags= fetch_all_img_tags(base_url)
download_image(img_tags, base_url)

