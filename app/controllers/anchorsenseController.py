from bs4 import BeautifulSoup
from typing import List
from ..utils.fetcher import fetch_html_with_selenium
from ..utils.tagfetcher.tagFetcherUtil import get_anchor_tags_from_html
from ..lib.anchorsense import analyze_anchor_tag

async def analyse_anchor_tag(url):

    html_content=fetch_html_with_selenium(url)
    # Retrieve all anchor tags from the HTML content
    anchor_tags = get_anchor_tags_from_html(html_content)
    
    all_issues = []
    # Iterate through each anchor tag to analyze it
    for anchor_tag in anchor_tags:
        issue_for_tag = analyze_anchor_tag(anchor_tag)
        all_issues.append(issue_for_tag)

    return all_issues
