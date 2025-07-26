import re
from typing import List, Dict, Union
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from bs4.element import Tag

# Assuming a utility function 'fetch_html_with_selenium' exists
# from utils.fetcher import fetch_html_with_selenium

def _check_descriptiveness(tag: Tag) -> List[str]:
    issues = []
    link_text = tag.get_text(strip=True).lower()
    
    has_image_with_alt = tag.find('img') and tag.find('img').get('alt', '').strip()
    if not link_text and not has_image_with_alt and not tag.has_attr('aria-label'):
         issues.append("Link has no descriptive text, image with alt text, or aria-label.")
         return issues

    non_descriptive_phrases = {
        "click here", "learn more", "read more", "go to", "link", "here", "more", "info"
    }

    if link_text in non_descriptive_phrases:
        issues.append("Link text is generic and non-descriptive (e.g., 'click here', 'learn more').")

    if len(link_text.split()) < 2 and not link_text.isdigit():
        issues.append("Link text consists of a single, non-numeric word which may lack context.")
        
    return issues

def _check_external_link_target(tag: Tag, base_netloc: str) -> List[str]:
    issues = []
    href = tag.get('href')
    if not href or not href.startswith(('http://', 'https://')):
        return issues
        
    try:
        link_netloc = urlparse(href).netloc
    except ValueError:
        return issues

    is_external = link_netloc and link_netloc != base_netloc
    
    if is_external and tag.get('target') == '_blank':
        text_content = tag.get_text(strip=True).lower()
        has_visual_indicator = any(indicator in text_content for indicator in ['(opens in new tab)', 'new window'])
        has_accessible_indicator = tag.has_attr('aria-label') or tag.has_attr('aria-labelledby')
        
        if not has_visual_indicator and not has_accessible_indicator:
            issues.append("External link opens in a new tab without a clear visual or ARIA indicator.")
            
    return issues

def _check_image_link(tag: Tag) -> List[str]:
    issues = []
    is_image_only_link = tag.find('img') and not tag.get_text(strip=True)
    
    if is_image_only_link:
        has_aria_label = tag.has_attr('aria-label') or tag.has_attr('aria-labelledby')
        img_tag = tag.find('img')
        has_img_alt = img_tag and img_tag.get('alt', '').strip() != ''
        
        if not has_aria_label and not has_img_alt:
            issues.append("Image-only link is missing an accessible name. Add 'alt' text to the image or an 'aria-label' to the link.")
            
    return issues

def _check_href_and_focus(tag: Tag) -> List[str]:
    issues = []
    if not tag.has_attr('href'):
        is_button_like = tag.get('role') == 'button' and tag.has_attr('tabindex')
        if not is_button_like:
            issues.append("Anchor tag is missing an 'href' attribute, making it non-interactive.")
    elif tag['href'].strip() in ('', '#'):
        issues.append("Anchor tag has a placeholder 'href' attribute.")

    if tag.get('tabindex') == '-1':
        issues.append("Anchor tag has 'tabindex=\"-1\"', removing it from keyboard navigation.")
        
    if tag.has_attr('disabled'):
        issues.append("Anchor tag uses the 'disabled' attribute, which is not valid and may not prevent interaction.")
        
    return issues

def _check_non_semantic_link(tag: Tag) -> List[str]:
    issues = [f"Non-semantic element ('{tag.name}') used as a link with 'onclick'."]
    
    if not tag.has_attr('role') or tag.get('role') not in ('link', 'button'):
        issues.append("Element is missing a 'role' of 'link' or 'button'.")
        
    if not tag.has_attr('tabindex') or int(tag.get('tabindex', -1)) < 0:
        issues.append("Element is missing 'tabindex=\"0\"' to be keyboard focusable.")
        
    if not any(tag.has_attr(attr) for attr in ['onkeydown', 'onkeyup', 'onkeypress']):
        issues.append("Element has 'onclick' but lacks a keyboard event handler (e.g., 'onkeydown').")
        
    return issues

def analyze_page_links(html_content: str, base_url: str) -> List[Dict[str, Union[str, List[str]]]]:
    soup = BeautifulSoup(html_content, 'html.parser')
    base_netloc = urlparse(base_url).netloc
    elements_with_issues = []

    for tag in soup.find_all('a'):
        tag_str = re.sub(r'\s+', ' ', str(tag)).strip()
        all_issues = []
        
        all_issues.extend(_check_descriptiveness(tag))
        all_issues.extend(_check_external_link_target(tag, base_netloc))
        all_issues.extend(_check_image_link(tag))
        all_issues.extend(_check_href_and_focus(tag))
        
        if all_issues:
            elements_with_issues.append({
                "issueElement": tag_str,
                "issues": all_issues
            })

    clickable_tags = soup.find_all(lambda t: t.has_attr('onclick') and t.name not in ['a', 'button', 'input'])
    for tag in clickable_tags:
        tag_str = re.sub(r'\s+', ' ', str(tag)).strip()
        all_issues = _check_non_semantic_link(tag)
        
        if all_issues:
             elements_with_issues.append({
                "issueElement": tag_str,
                "issues": all_issues
            })

    return elements_with_issues

def link_analysis_controller(url: str):
    # html_content = fetch_html_with_selenium(url)
    # This is a placeholder for your actual fetcher
    html_content = f'<html><body><a href="{url}/about">About</a><a href="#"></a><a></a><a href="https://example.com" target="_blank">External</a></body></html>'

    if not html_content:
        return {"error": f"Failed to fetch HTML content from {url}."}

    parsed_url = urlparse(url)
    if not parsed_url.scheme or not parsed_url.netloc:
         return {"error": f"Invalid URL provided: {url}."}
    
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    analysis_results = analyze_page_links(html_content, base_url)
    
    return analysis_results
def fetch_anchor_tags(html_content):
    #use beautify soup to fetch all the anchor tags and return an list
def analyse_link_attribute(html_content):
    data=html_content
    anchor_tags= fetch_anchor_tags(data)
    #take an anchor tag and loop it to find these 
    #Function for is_descriptive (which analyse the anchor tag and return yes,no,notapplicable )
    is_descriptive=
    is_ExtBlank=
    is_href=
    is_img_Aria=
    is_key_nav=
    
    #once i have the value of these 
    '''
    add this create an object of each 
    {
        element:"<a><a>",
        
    }
    '''
    
    