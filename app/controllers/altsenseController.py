from bs4 import BeautifulSoup
from typing import List, Optional, Dict
from ..utils.fetcher import fetch_html_with_selenium
from ..utils.tagfetcher.tagFetcherUtil import get_img_tags_from_html
from ..lib.altsenelib import analyze_image_tag

async def analyze_alt_attributes_controller(url: str) -> Optional[List[Dict]]:
    html_content = await fetch_html_with_selenium(url)
    if not html_content:
        return None  # Indicate failure to fetch
    
    img_tags = get_img_tags_from_html(html_content)

    all_issues = []
    for img_tag in img_tags:
        issues_for_tag = analyze_image_tag(img_tag)
        all_issues.extend(issues_for_tag)

    return all_issues


def analyze_alt_attributes_from_html_controller(html_content: str) -> List[Dict]:
    """
    Analyze alt attributes from HTML content directly (for file uploads)
    
    Args:
        html_content: The HTML content as string
        
    Returns:
        List of issues found in the HTML
    """
    img_tags = get_img_tags_from_html(html_content)

    all_issues = []
    for img_tag in img_tags:
        issues_for_tag = analyze_image_tag(img_tag)
        all_issues.extend(issues_for_tag)

    return all_issues