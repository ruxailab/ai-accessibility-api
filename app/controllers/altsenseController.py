from bs4 import BeautifulSoup
from typing import List
from ..utils.fetcher import fetch_html_with_selenium
from ..utils.tagfetcher.tagFetcherUtil import get_img_tags_from_html
from ..lib.altsenelib import analyze_image_tag

async def analyze_alt_attributes_controller(url: str):
    html_content = fetch_html_with_selenium(url)
    if not html_content:
        return None # Indicate failure to fetch
    
    #find all the img tag
    img_tags=get_img_tags_from_html(html_content)
    
    all_issues=[]
    for img_tag in img_tags:
        issue_for_tag=analyze_image_tag(img_tag)
        all_issues.extend(issue_for_tag)

    return all_issues