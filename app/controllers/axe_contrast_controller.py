"""
Controllers for Axe-Core Color Contrast Checking
"""

from typing import Dict
from app.lib.axe_contrast_checker import check_url_contrast, check_html_contrast


async def examine_url_contrast(url: str, add_markers: bool = True) -> Dict:
    """
    Check color contrast issues on a URL using axe-core
    
    Args:
        url: URL to analyze
        add_markers: Whether to add visual markers to HTML
        
    Returns:
        Dictionary with violations and optionally marked HTML
    """
    result = check_url_contrast(url, add_markers=add_markers)
    return result


async def examine_html_contrast(html_content: str, add_markers: bool = True) -> Dict:
    """
    Check color contrast issues in HTML content using axe-core
    
    Args:
        html_content: HTML string to analyze
        add_markers: Whether to add visual markers to HTML
        
    Returns:
        Dictionary with violations and optionally marked HTML
    """
    result = check_html_contrast(html_content, add_markers=add_markers)
    return result
