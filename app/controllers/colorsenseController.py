"""
ColorSense Controller - Handles color contrast analysis requests
"""

from typing import Dict, Optional
from ..lib.colorsense import ColorContrastAnalyzer
from ..utils.fetcher import fetch_html_with_selenium


async def analyze_color_contrast_controller(url: str, add_tooltips: bool = False) -> Optional[Dict]:
    """
    Controller to analyze color contrast issues in a webpage
    
    Args:
        url: The URL of the webpage to analyze
        add_tooltips: Whether to return HTML with tooltip markers
        
    Returns:
        Dictionary containing analysis results and optionally marked HTML
    """
    try:
        # Fetch HTML content
        html_content = await fetch_html_with_selenium(url)
        
        if not html_content:
            return None
        
        # Initialize analyzer
        analyzer = ColorContrastAnalyzer()
        
        # Analyze the HTML
        analysis_result = analyzer.analyze_html(html_content)
        
        # Prepare response
        response = {
            'url': url,
            'analysis': analysis_result
        }
        
        # Add marked HTML if requested
        if add_tooltips:
            marked_html = analyzer.add_tooltips_to_html(
                html_content, 
                analysis_result['issues']
            )
            response['marked_html'] = marked_html
        
        return response
        
    except Exception as e:
        print(f"Error in analyze_color_contrast_controller: {str(e)}")
        return None


async def analyze_html_contrast_controller(html_content: str, add_tooltips: bool = False) -> Optional[Dict]:
    """
    Controller to analyze color contrast issues in HTML content provided directly
    
    Args:
        html_content: The HTML content to analyze
        add_tooltips: Whether to return HTML with tooltip markers
        
    Returns:
        Dictionary containing analysis results and optionally marked HTML
    """
    try:
        if not html_content or not html_content.strip():
            return None
        
        # Initialize analyzer
        analyzer = ColorContrastAnalyzer()
        
        # Analyze the HTML
        analysis_result = analyzer.analyze_html(html_content)
        
        # Prepare response
        response = {
            'source': 'user_provided_html',
            'analysis': analysis_result
        }
        
        # Add marked HTML if requested
        if add_tooltips:
            marked_html = analyzer.add_tooltips_to_html(
                html_content, 
                analysis_result['issues']
            )
            response['marked_html'] = marked_html
        
        return response
        
    except Exception as e:
        print(f"Error in analyze_html_contrast_controller: {str(e)}")
        return None
