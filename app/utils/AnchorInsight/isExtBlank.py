from bs4 import BeautifulSoup
def check_external_links(html_content):
    """
    Checks if external links have a target="_blank" attribute and an indication
    that they open in a new tab.

    Args:
        html_content (str): The HTML content to check.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    anchor_tags = soup.find_all('a')

    from bs4.element import Tag
    for tag in anchor_tags:
        if isinstance(tag, Tag) and tag.has_attr('target') and tag['target'] == '_blank':
            # Check for text indicating a new tab
            if '(opens in new tab)' not in tag.get_text() and not tag.has_attr('aria-label'):
                print(f"Potential Issue: External link without new tab indication: {tag}")

# Run the check on the HTML content from the website
check_external_links(html_content)