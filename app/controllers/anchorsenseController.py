import logging
from bs4 import BeautifulSoup
from typing import List
from ..utils.fetcher import fetch_html_with_selenium # This is now async
from ..utils.tagfetcher.tagFetcherUtil import get_anchor_tags_from_html
from ..lib.anchorsense import analyze_anchor_tag

logger = logging.getLogger(__name__)

async def analyse_anchor_tag(url):
    logger.debug("Fetching HTML content from %s", url)
    # Await the asynchronous fetch_html_with_selenium function
    html_content = await fetch_html_with_selenium(url)
  
    logger.debug("HTML content fetched successfully")

    if html_content is None:
        logger.error("Failed to fetch HTML content for %s", url)
        return [] # Or raise an error, depending on desired behavior

    logger.debug("Retrieving anchor tags from HTML")
    anchor_tags = get_anchor_tags_from_html(html_content)
    logger.debug("Found %d anchor tags (type: %s)", len(anchor_tags), type(anchor_tags).__name__)
    all_issues = []
    for anchor_tag in anchor_tags:
        try:
            issue_for_tag = analyze_anchor_tag(anchor_tag)
            all_issues.extend(issue_for_tag)
        except Exception as e:
            logger.exception("Error analyzing anchor tag: %s", anchor_tag)


    return all_issues


def analyse_anchor_tag_from_html(html_content: str) -> List:
    """
    Analyze anchor tags from HTML content directly (for file uploads)
    
    Args:
        html_content: The HTML content as string
        
    Returns:
        List of issues found in the HTML
    """
    logger.debug("Retrieving anchor tags from HTML content")
    anchor_tags = get_anchor_tags_from_html(html_content)
    logger.debug("Found %d anchor tags (type: %s)", len(anchor_tags), type(anchor_tags).__name__)
    
    all_issues = []
    for anchor_tag in anchor_tags:
        try:
            issue_for_tag = analyze_anchor_tag(anchor_tag)
            all_issues.extend(issue_for_tag)
        except Exception as e:
            logger.exception("Error analyzing anchor tag: %s", anchor_tag)

    return all_issues