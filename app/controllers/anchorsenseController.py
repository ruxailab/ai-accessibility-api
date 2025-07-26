from bs4 import BeautifulSoup
from typing import List
from ..utils.fetcher import fetch_html_with_selenium # This is now async
from ..utils.tagfetcher.tagFetcherUtil import get_anchor_tags_from_html
from ..lib.anchorsense import analyze_anchor_tag

async def analyse_anchor_tag(url):
    print("fetching html-content")
    # Await the asynchronous fetch_html_with_selenium function
    html_content = await fetch_html_with_selenium(url)
  
    print("html content fetched")

    if html_content is None:
        print(f"Failed to fetch HTML content for {url}")
        return [] # Or raise an error, depending on desired behavior

    print("retrieving anchor tags")
    anchor_tags = get_anchor_tags_from_html(html_content)
    print(f"Type of anchor_tags: {type(anchor_tags)}, Length: {len(anchor_tags)}")
    print("anchor tag processed")
    all_issues = []
    for anchor_tag in anchor_tags:
        try:
            issue_for_tag = analyze_anchor_tag(anchor_tag)
            all_issues.append(issue_for_tag)
        except Exception as e:
            print(f"Error analyzing tag: {anchor_tag}, Error: {e}")


    return all_issues