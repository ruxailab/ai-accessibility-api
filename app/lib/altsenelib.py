from bs4 import BeautifulSoup

def analyze_image_tag(tag):
    issues = []

    # 1. Check if alt attribute is missing
    def is_alt_missing(tag):
        return not tag.has_attr('alt')

    # 2. Check if alt text is vague
    def is_alt_vague(tag):
        vague_terms = ['image', 'photo', 'picture', 'graphic']
        alt_text = tag.get('alt', '').strip().lower()
        return alt_text in vague_terms or len(alt_text) < 3

    # Apply checks
    if is_alt_missing(tag):
        issues.append({
            "module": "imagealt",
            "element": str(tag),
            "issue": "Missing alt attribute on image",
            "help": "Add a meaningful alt attribute to describe the image for screen readers."
        })
    elif is_alt_vague(tag):
        issues.append({
            "module": "imagealt",
            "element": str(tag),
            "issue": "Vague alt text",
            "help": "Avoid vague alt text like 'image' or 'photo'; describe the image content clearly."
        })

    return issues
