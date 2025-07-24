from bs4 import BeautifulSoup

def check_image_links_for_aria_label(html_content):
    """
    Checks if image-only links have an aria-label or aria-labelledby attribute.

    Args:
        html_content (str): The HTML content to check.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    anchor_tags = soup.find_all('a')

    for tag in anchor_tags:
        # Check if the link contains an image
        if tag.find('img'):
            # Check if the link contains *only* an image (no significant text content)
            # This is more robust than just tag.get_text(strip=True)
            has_only_image = True
            for content in tag.contents:
                if content.name != 'img' and str(content).strip():
                    has_only_image = False
                    break

            if has_only_image:
                # Ensure tag is a BeautifulSoup Tag before checking attributes
                from bs4 import Tag
                if isinstance(tag, Tag):
                    if tag.get('aria-label') is None and tag.get('aria-labelledby') is None:
                        print(f"Potential Issue: Image-only link without aria-label or aria-labelledby: {tag}")
