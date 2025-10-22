"""
Axe-Core Color Contrast Checker
Uses axe-core for robust accessibility testing
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from axe_selenium_python import Axe
from bs4 import BeautifulSoup
import json
import tempfile
import os
from typing import Dict, List, Optional


class AxeColorContrastChecker:
    """
    Color contrast checker using axe-core
    More robust and industry-standard than custom implementation
    """
    
    def __init__(self):
        """Initialize the checker"""
        self.driver = None
    
    def _setup_driver(self):
        """Setup headless Chrome driver"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
    
    def _cleanup_driver(self):
        """Close the driver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def check_url(self, url: str) -> Dict:
        """
        Check color contrast issues on a URL
        
        Args:
            url: URL to check
            
        Returns:
            Dictionary with violations
        """
        try:
            self._setup_driver()
            self.driver.get(url)
            
            # Run axe-core with ONLY color-contrast rule (much faster!)
            axe = Axe(self.driver)
            axe.inject()
            
            # Run only color-contrast related rules
            results = axe.run(options={
                "runOnly": {
                    "type": "rule",
                    "values": ["color-contrast"]
                }
            })
            
            # Filter for color contrast issues
            color_issues = self._filter_color_contrast_issues(results)
            
            return {
                'url': url,
                'violations': color_issues,
                'total_issues': len(color_issues),
                'passed': len(color_issues) == 0
            }
            
        finally:
            self._cleanup_driver()
    
    def check_html(self, html_content: str) -> Dict:
        """
        Check color contrast issues in HTML content
        
        Args:
            html_content: HTML string to check
            
        Returns:
            Dictionary with violations
        """
        try:
            self._setup_driver()
            
            # Save HTML to temp file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
                f.write(html_content)
                temp_path = f.name
            
            # Load the file
            self.driver.get(f'file://{temp_path}')
            
            # Run axe-core with ONLY color-contrast rule (much faster!)
            axe = Axe(self.driver)
            axe.inject()
            
            # Run only color-contrast related rules
            results = axe.run(options={
                "runOnly": {
                    "type": "rule",
                    "values": ["color-contrast"]
                }
            })
            
            # Filter for color contrast issues
            color_issues = self._filter_color_contrast_issues(results)
            
            # Clean up temp file
            os.unlink(temp_path)
            
            return {
                'source': 'html_content',
                'violations': color_issues,
                'total_issues': len(color_issues),
                'passed': len(color_issues) == 0
            }
            
        finally:
            self._cleanup_driver()
    
    def _filter_color_contrast_issues(self, axe_results: Dict) -> List[Dict]:
        """
        Filter and format color contrast issues from axe results
        
        Args:
            axe_results: Full axe-core results
            
        Returns:
            List of color contrast violations
        """
        color_issues = []
        
        violations = axe_results.get('violations', [])
        
        for violation in violations:
            # Only include color-contrast related rules
            if 'color-contrast' in violation.get('id', ''):
                nodes = violation.get('nodes', [])
                
                for node in nodes:
                    issue = {
                        'rule_id': violation.get('id'),
                        'description': violation.get('description'),
                        'help': violation.get('help'),
                        'help_url': violation.get('helpUrl'),
                        'impact': node.get('impact', 'unknown'),
                        'element': {
                            'html': node.get('html', ''),
                            'target': node.get('target', []),
                        },
                        'failure_summary': node.get('failureSummary', ''),
                        'message': node.get('any', [{}])[0].get('message', '') if node.get('any') else ''
                    }
                    color_issues.append(issue)
        
        return color_issues
    
    def add_visual_markers(self, html_content: str, violations: List[Dict]) -> str:
        """
        Add simple visual markers to HTML for color contrast issues
        
        Args:
            html_content: Original HTML
            violations: List of violations from axe-core
            
        Returns:
            HTML with visual markers
        """
        if not violations:
            return html_content
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Add styles for markers
        style_tag = soup.new_tag('style')
        style_tag.string = """
        /* Axe-Core Color Contrast Issue Markers */
        .axe-contrast-issue {
            outline: 3px solid red !important;
            position: relative !important;
        }
        .axe-contrast-tooltip {
            position: absolute !important;
            background: #ff0000 !important;
            color: white !important;
            padding: 5px 10px !important;
            border-radius: 3px !important;
            font-size: 12px !important;
            z-index: 10000 !important;
            top: -30px !important;
            left: 0 !important;
            white-space: nowrap !important;
            display: none !important;
        }
        .axe-contrast-issue:hover .axe-contrast-tooltip {
            display: block !important;
        }
        """
        
        if soup.head:
            soup.head.append(style_tag)
        else:
            head = soup.new_tag('head')
            head.append(style_tag)
            if soup.html:
                soup.html.insert(0, head)
        
        # Mark each violation
        for idx, violation in enumerate(violations):
            element_html = violation['element']['html']
            impact = violation['impact']
            message = violation.get('failure_summary', violation.get('message', 'Color contrast issue'))
            
            # Try to find and mark the element
            # This is a simple approach - find by HTML content
            try:
                # Extract tag name and some attributes for matching
                temp_soup = BeautifulSoup(element_html, 'html.parser')
                if temp_soup and temp_soup.contents:
                    target_tag = temp_soup.contents[0]
                    tag_name = target_tag.name if hasattr(target_tag, 'name') else None
                    
                    if tag_name:
                        # Find similar elements
                        elements = soup.find_all(tag_name)
                        
                        for elem in elements:
                            elem_str = str(elem)
                            # Simple matching - can be improved
                            if element_html in elem_str or elem.get_text(strip=True) in element_html:
                                # Add class and tooltip
                                if 'class' in elem.attrs:
                                    elem['class'].append('axe-contrast-issue')
                                else:
                                    elem['class'] = ['axe-contrast-issue']
                                
                                # Add tooltip
                                tooltip = soup.new_tag('span', **{'class': 'axe-contrast-tooltip'})
                                tooltip.string = f"⚠ {impact.upper()}: Contrast issue"
                                elem.insert(0, tooltip)
                                break
            except Exception as e:
                # Skip if we can't mark this element
                continue
        
        return str(soup)


def check_url_contrast(url: str, add_markers: bool = False) -> Dict:
    """
    Check color contrast on a URL using axe-core
    
    Args:
        url: URL to check
        add_markers: Whether to return HTML with visual markers
        
    Returns:
        Dictionary with violations and optionally marked HTML
    """
    checker = AxeColorContrastChecker()
    result = checker.check_url(url)
    
    if add_markers and result['violations']:
        # Get the page HTML
        try:
            checker._setup_driver()
            checker.driver.get(url)
            html = checker.driver.page_source
            marked_html = checker.add_visual_markers(html, result['violations'])
            result['marked_html'] = marked_html
        finally:
            checker._cleanup_driver()
    
    return result


def check_html_contrast(html_content: str, add_markers: bool = False) -> Dict:
    """
    Check color contrast in HTML content using axe-core
    
    Args:
        html_content: HTML string to check
        add_markers: Whether to return HTML with visual markers
        
    Returns:
        Dictionary with violations and optionally marked HTML
    """
    checker = AxeColorContrastChecker()
    result = checker.check_html(html_content)
    
    if add_markers and result['violations']:
        marked_html = checker.add_visual_markers(html_content, result['violations'])
        result['marked_html'] = marked_html
    
    return result


# Example usage
if __name__ == "__main__":
    print("=" * 80)
    print("Axe-Core Color Contrast Checker Demo")
    print("=" * 80)
    print()
    
    # Test with sample HTML
    test_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Page</title>
    </head>
    <body>
        <h1 style="color: #777; background: #fff;">Medium Contrast Title</h1>
        <p style="color: #ccc; background: #fff;">Very Low Contrast Paragraph</p>
        <p style="color: #000; background: #fff;">Good Contrast Paragraph</p>
        <button style="color: #fff; background: #ffff00;">Bad Button</button>
    </body>
    </html>
    """
    
    print("Testing HTML content...")
    print("-" * 80)
    
    result = check_html_contrast(test_html, add_markers=True)
    
    print(f"Total Issues Found: {result['total_issues']}")
    print(f"Passed: {result['passed']}")
    print()
    
    if result['violations']:
        print("Violations:")
        for i, violation in enumerate(result['violations'], 1):
            print(f"\n{i}. {violation['description']}")
            print(f"   Impact: {violation['impact'].upper()}")
            print(f"   Element: {violation['element']['html'][:100]}...")
            print(f"   Issue: {violation['failure_summary'][:150]}...")
    
    if 'marked_html' in result:
        print("\n" + "-" * 80)
        print("✓ Marked HTML generated")
        print("  Save result['marked_html'] to a file to see visual markers")
    
    print("\n" + "=" * 80)
