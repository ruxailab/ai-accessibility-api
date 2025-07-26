from bs4 import BeautifulSoup
from typing import List
from utils.fetcher import fetch_html_with_selenium

def fetch_all_img_tags(html_content: str) -> List[str]:
    soup = BeautifulSoup(html_content, 'html.parser')
    img_tags = soup.find_all('img')
    return [str(tag) for tag in img_tags]

def find_problematic_img_tags(html_content: str) -> List[str]:
    soup = BeautifulSoup(html_content, 'html.parser')
    img_tags = soup.find_all('img')
    problematic_tags = []
    non_descriptive_alts = ["", "image", "img", "picture", "here"] # Add more as needed

    for tag in img_tags:
        alt_attribute = tag.get('alt')
        if alt_attribute is None or alt_attribute.strip() == "" or alt_attribute.strip().lower() in non_descriptive_alts:
            problematic_tags.append(str(tag))
    return problematic_tags

async def analyze_alt_attributes_controller(url: str):
    html_content = fetch_html_with_selenium(url)
    if not html_content:
        return None # Indicate failure to fetch

    all_img_tags = fetch_all_img_tags(html_content)
    problematic_img_tags = find_problematic_img_tags(html_content)
    
    return {
        "url": url,
        "total_images_found": len(all_img_tags),
        "all_img_tags": all_img_tags,
        "problematic_img_tags": problematic_img_tags,
        "num_problematic_img_tags": len(problematic_img_tags)
    }