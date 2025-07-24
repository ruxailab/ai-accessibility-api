import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

HEADING_TAGS = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
VISUAL_HEADING_KEYWORDS = ['title', 'header', 'heading', 'section-title']

def fetch_html(source):
    if urlparse(source).scheme in ['http', 'https']:
        try:
            response = requests.get(source, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {source}: {e}")
            return ""
    else:
        with open(source, 'r', encoding='utf-8') as f:
            return f.read()

def get_headings(soup):
    return [(tag.name, tag.get_text(strip=True), tag) for tag in soup.find_all(HEADING_TAGS)]

def detect_heading_issues(headings):
    issues = []
    levels = [int(tag[0][1]) for tag in headings]

    # Check for missing <h1>
    h1_count = levels.count(1)
    if h1_count == 0:
        issues.append({
            "issue": "Missing <h1>",
            "suggestion": "Add a single <h1> to represent the main page title."
        })
    elif h1_count > 1:
        issues.append({
            "issue": "Multiple <h1> tags",
            "suggestion": "Use only one <h1> for the page title. Use <h2> or below for other sections."
        })

    # Check for skipped levels
    for i in range(1, len(levels)):
        if levels[i] > levels[i - 1] + 1:
            issues.append({
                "issue": "Skipped heading level",
                "context": str(headings[i][2]),
                "suggestion": f"Replace <h{levels[i]}> with <h{levels[i - 1] + 1}> to maintain hierarchy."
            })

    return issues

def detect_visual_headings(soup):
    issues = []
    for tag in soup.find_all(['div', 'span']):
        class_attr = tag.get('class')
        if class_attr:
            if any(any(k in c.lower() for k in VISUAL_HEADING_KEYWORDS) for c in class_attr):
                issues.append({
                    "issue": "Non-semantic visual heading",
                    "context": str(tag),
                    "suggestion": "Use semantic tags like <h2>–<h6> instead of styled <div>/<span> for headings."
                })
    return issues

def run_heading_checker(source):
    html = fetch_html(source)
    if not html:
        print("No content found.")
        return

    soup = BeautifulSoup(html, 'html.parser')
    headings = get_headings(soup)

    issues = detect_heading_issues(headings)
    visual_issues = detect_visual_headings(soup)

    print(f"\n🔍 Found {len(headings)} headings.")
    print(f"📋 Reporting {len(issues) + len(visual_issues)} issues...\n")

    for i, issue in enumerate(issues + visual_issues, 1):
        print(f"Issue {i}: {issue['issue']}")
        if "context" in issue:
            print("Context:", issue["context"])
        print("Suggestion:", issue["suggestion"])
        print("-" * 60)

if __name__ == "__main__":
    source = input("Enter a URL or local HTML file path: ").strip()
    run_heading_checker(source)
