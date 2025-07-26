from urllib.parse import urlparse

def get_pa11y_style_context(tag, max_len=300):
    html = str(tag)
    return html if len(html) <= max_len else html[:max_len] + "... [truncated]"

def analyze_anchor_tag(tag):  # tag is already a BS4 element
    issues = []

    # 1. Check if link is descriptive
    def is_descriptive_link(tag):
        link_text = tag.get_text(strip=True).lower()
        non_descriptive = ["click here", "learn more", "read more", "go to", "link", "here", "more", "info"]
        if link_text in non_descriptive or len(link_text.split()) < 2:
            return False
        return True

    # 2. Check if it's an external link and target is _blank
    def is_external_with_blank(tag):
        if tag.has_attr('href'):
            href = tag['href']
            parsed = urlparse(href)
            if parsed.scheme in ('http', 'https') and tag.get('target') != '_blank':
                return False
        return True

    # 3. Not used as a button
    def is_valid_link(tag):
        if not tag.has_attr('href'):
            if not (tag.has_attr('role') and tag['role'] == 'button' and tag.has_attr('tabindex')):
                return False
        elif tag['href'] in ('', '#'):
            return False
        return True

    # 4. Keyboard navigable
    def is_keyboard_accessible(tag):
        if tag.has_attr('tabindex') and tag['tabindex'] == '-1':
            return False
        if tag.has_attr('disabled'):
            return False
        return True

    # Use compact version for logging/report
    context = get_pa11y_style_context(tag)

    if not is_descriptive_link(tag):
        issues.append({
            "code": 1,
            "module": "anchorInsight",
            "element": context,
            "issue": "Non-descriptive anchor text",
            "help": "Use meaningful link text that describes the destination or action."
        })

    if not is_external_with_blank(tag):
        issues.append({
            "code": 2,
            "module": "anchorInsight",
            "element": context,
            "issue": "External link missing target='_blank'",
            "help": "Add target='_blank' to open external links in a new tab."
        })

    if not is_valid_link(tag):
        issues.append({
            "code": 3,
            "module": "anchorInsight",
            "element": context,
            "issue": "Anchor used as button or missing href",
            "help": "Use <button> for actions, or ensure proper role and tabindex if using <a>."
        })

    if not is_keyboard_accessible(tag):
        issues.append({
            "code": 4,
            "module": "anchorInsight",
            "element": context,
            "issue": "Anchor is not keyboard navigable",
            "help": "Ensure anchor is focusable using correct tabindex and avoid disabled attribute."
        })

    return issues
