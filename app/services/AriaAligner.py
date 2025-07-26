from bs4 import BeautifulSoup

def analyze_aria_labels(html):
    soup = BeautifulSoup(html, 'html.parser')
    issues = []

    def add_issue(tag, message, help_text):
        issues.append({
            "module": "ariaaligner",
            "element": str(tag),
            "issue": message,
            "help": help_text
        })

    # 1. Button without visible text
    for tag in soup.find_all('button'):
        if not tag.get_text(strip=True) and not tag.has_attr('aria-label'): # type: ignore
            add_issue(tag, "Button has no text or aria-label", "Add an aria-label to buttons without visible text.")

    # 2. Input without associated label or aria-label
    for tag in soup.find_all('input'):
        if not tag.has_attr('aria-label') and not tag.has_attr('aria-labelledby'): # type: ignore
            label = soup.find('label', attrs={'for': tag.get('id')})
            if label is None:
                add_issue(tag, "Input is missing associated label or ARIA label", "Use <label> or aria-label/aria-labelledby for accessibility.")

    # 3. Anchor without visible text or aria-label
    for tag in soup.find_all('a'):
        if not tag.get_text(strip=True) and not tag.has_attr('aria-label'):
            add_issue(tag, "Anchor tag has no visible text or aria-label", "Add aria-label for links without visible text.")

    # 4. Nav without aria-label when there are multiple navs
    navs = soup.find_all('nav')
    if len(navs) > 1:
        for tag in navs:
            if not tag.has_attr('aria-label') and not tag.has_attr('aria-labelledby'):
                add_issue(tag, "Multiple <nav> tags found but missing aria-label", "Use aria-label to describe the purpose of each <nav> region.")

    # 5. Anchor with redundant aria-label
    for tag in soup.find_all('a'):
        if tag.has_attr('aria-label'):
            text = tag.get_text(strip=True).lower()
            aria = tag['aria-label'].strip().lower()
            if text and text in aria:
                add_issue(tag, "Redundant aria-label", "Avoid duplicating visible link text in aria-label.")

    return issues


# Test cases
html_snippets = [
    '<button><svg></svg></button>',
    '<input type="text" aria-label="Search website">',
    '<a href="/download" aria-label="Download PDF"><i class="fa fa-download"></i></a>',
    '<nav aria-label="Main navigation">...</nav>',
    '<a href="/about" aria-label="Learn more about us">About</a>'
]

for snippet in html_snippets:
    result = analyze_aria_labels(snippet)
    for r in result:
        print(r)