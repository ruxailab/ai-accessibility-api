from bs4 import BeautifulSoup
def check_for_non_semantic_links(html_content):
    """
    Checks for non-semantic elements (divs and spans) with onclick handlers.

    Args:
        html_content (str): The HTML content to check.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all div and span tags with an onclick attribute
    non_semantic_tags = soup.find_all(['div', 'span'], onclick=True)
    
    for tag in non_semantic_tags:
        print(f"Potential Issue: Non-semantic tag with onclick handler: {tag}")

# Run the check on the HTML content from the website
check_for_non_semantic_links(html_content)