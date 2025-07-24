import requests
from bs4 import BeautifulSoup

def fetch_all_anchor_tags(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    anchor_tags = soup.find_all('a')
    return anchor_tags

def is_descriptive_link(anchor_tag):
    """
    Checks if the text of an anchor tag is descriptive.

    Args:
        anchor_tag (bs4.element.Tag): A BeautifulSoup anchor tag.

    Returns:
        bool: True if the link text is descriptive, False otherwise.
    """
    link_text = anchor_tag.get_text(strip=True).lower()

    # List of common non-descriptive phrases
    non_descriptive_phrases = [
        "click here",
        "learn more",
        "read more",
        "go to",
        "link",
        "here",
        "more",
        "info"
    ]

    # Check if the link text is one of the non-descriptive phrases
    if link_text in non_descriptive_phrases:
        return False

    # Check if the link text is too short
    if len(link_text.split()) < 2:
        return False

    return True

anchor_tags=[]
# Test the function with the anchor tags from the website
for tag in anchor_tags:
    if is_descriptive_link(tag):
        print(f"Good link text: '{tag.get_text(strip=True)}'")
    else:
        print(f"Bad link text: '{tag.get_text(strip=True)}'")