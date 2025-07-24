from bs4 import BeautifulSoup
def check_keyboard_navigability(html_content):
    """
    Checks for common HTML attributes that can affect keyboard navigability.

    Args:
        html_content (str): The HTML content to check.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    anchor_tags = soup.find_all('a')

    for tag in anchor_tags:
        # Check for tabindex="-1", which removes the element from the tab order
        if tag.has_attr('tabindex') and tag['tabindex'] == '-1':
            print(f"Potential Issue: Anchor tag with tabindex='-1': {tag}")

        # Check for the disabled attribute, which can make the link unfocusable
        if tag.has_attr('disabled'):
            print(f"Potential Issue: Disabled anchor tag: {tag}")
