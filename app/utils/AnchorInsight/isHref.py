from bs4 import BeautifulSoup

def check_anchor_tags_for_accessibility(html_content):
    """
    Checks for common issues with anchor tags in HTML content,
    considering accessibility best practices.

    Args:
        html_content (str): The HTML content to check.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    anchor_tags = soup.find_all('a')

    from bs4 import Tag

    for tag in anchor_tags:
        if isinstance(tag, Tag):
            if not tag.has_attr('href'):
                # Check for ARIA role and tabindex if href is missing
                if not (tag.has_attr('role') and tag['role'] == 'button' and tag.has_attr('tabindex')):
                    print(f"Issue: Anchor tag without href, role='button', and tabindex: {tag}")
            elif tag['href'] in ('', '#'):
                print(f"Issue: Anchor tag with empty or placeholder href: {tag}")
