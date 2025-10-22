"""
ColorSense Library - Analyzes color contrast issues in HTML
Checks WCAG 2.1 compliance for text and background color combinations
"""

import re
from typing import List, Dict, Tuple, Optional
from bs4 import BeautifulSoup
import colorsys


class ColorContrastAnalyzer:
    """Analyzes color contrast ratios according to WCAG 2.1 guidelines"""
    
    # WCAG 2.1 Level AA requirements
    WCAG_AA_NORMAL = 4.5  # Normal text
    WCAG_AA_LARGE = 3.0   # Large text (18pt+ or 14pt+ bold)
    
    # WCAG 2.1 Level AAA requirements
    WCAG_AAA_NORMAL = 7.0  # Normal text
    WCAG_AAA_LARGE = 4.5   # Large text
    
    def __init__(self):
        pass
    
    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        
        # Handle shorthand hex colors (#fff -> #ffffff)
        if len(hex_color) == 3:
            hex_color = ''.join([c*2 for c in hex_color])
        
        try:
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        except ValueError:
            return (0, 0, 0)  # Default to black if invalid
    
    @staticmethod
    def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
        """Convert RGB tuple to hex color"""
        return '#{:02x}{:02x}{:02x}'.format(*rgb)
    
    @staticmethod
    def get_relative_luminance(rgb: Tuple[int, int, int]) -> float:
        """Calculate relative luminance according to WCAG formula"""
        def adjust_channel(channel: int) -> float:
            c = channel / 255.0
            if c <= 0.03928:
                return c / 12.92
            return ((c + 0.055) / 1.055) ** 2.4
        
        r, g, b = [adjust_channel(c) for c in rgb]
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    
    @staticmethod
    def calculate_contrast_ratio(color1: Tuple[int, int, int], 
                                 color2: Tuple[int, int, int]) -> float:
        """
        Calculate contrast ratio between two colors
        Returns a value between 1 and 21
        """
        lum1 = ColorContrastAnalyzer.get_relative_luminance(color1)
        lum2 = ColorContrastAnalyzer.get_relative_luminance(color2)
        
        lighter = max(lum1, lum2)
        darker = min(lum1, lum2)
        
        return (lighter + 0.05) / (darker + 0.05)
    
    @staticmethod
    def parse_color(color_str: str) -> Optional[Tuple[int, int, int]]:
        """Parse various color formats to RGB"""
        if not color_str or color_str.lower() in ['transparent', 'inherit', 'initial', 'unset']:
            return None
        
        color_str = color_str.strip().lower()
        
        # Hex color
        if color_str.startswith('#'):
            return ColorContrastAnalyzer.hex_to_rgb(color_str)
        
        # RGB/RGBA
        rgb_match = re.match(r'rgba?\((\d+),\s*(\d+),\s*(\d+)', color_str)
        if rgb_match:
            return tuple(int(x) for x in rgb_match.groups())
        
        # Named colors (common ones)
        named_colors = {
            'white': (255, 255, 255), 'black': (0, 0, 0),
            'red': (255, 0, 0), 'green': (0, 128, 0), 'blue': (0, 0, 255),
            'yellow': (255, 255, 0), 'cyan': (0, 255, 255), 'magenta': (255, 0, 255),
            'gray': (128, 128, 128), 'grey': (128, 128, 128),
            'silver': (192, 192, 192), 'maroon': (128, 0, 0),
            'olive': (128, 128, 0), 'lime': (0, 255, 0), 'aqua': (0, 255, 255),
            'teal': (0, 128, 128), 'navy': (0, 0, 128), 'fuchsia': (255, 0, 255),
            'purple': (128, 0, 128), 'orange': (255, 165, 0)
        }
        
        if color_str in named_colors:
            return named_colors[color_str]
        
        return None
    
    @staticmethod
    def get_computed_colors(element, parent_bg: Optional[Tuple[int, int, int]] = None) -> Dict:
        """Extract computed foreground and background colors from element"""
        result = {
            'foreground': None,
            'background': None
        }
        
        style = element.get('style', '')
        
        # Parse inline styles
        if style:
            color_match = re.search(r'color:\s*([^;]+)', style, re.IGNORECASE)
            if color_match:
                result['foreground'] = ColorContrastAnalyzer.parse_color(color_match.group(1))
            
            bg_match = re.search(r'background(?:-color)?:\s*([^;]+)', style, re.IGNORECASE)
            if bg_match:
                result['background'] = ColorContrastAnalyzer.parse_color(bg_match.group(1))
        
        # Default text color is black
        if result['foreground'] is None:
            result['foreground'] = (0, 0, 0)
        
        # Default background is white or inherited from parent
        if result['background'] is None:
            result['background'] = parent_bg if parent_bg else (255, 255, 255)
        
        return result
    
    @staticmethod
    def is_large_text(element) -> bool:
        """Determine if text should be considered large text for WCAG"""
        style = element.get('style', '')
        
        # Check for bold
        is_bold = False
        if 'font-weight:' in style:
            weight_match = re.search(r'font-weight:\s*(\w+)', style, re.IGNORECASE)
            if weight_match:
                weight = weight_match.group(1)
                is_bold = weight in ['bold', 'bolder', '700', '800', '900']
        
        # Check for large font
        is_large = element.name in ['h1', 'h2', 'h3']
        if 'font-size:' in style:
            size_match = re.search(r'font-size:\s*([\d.]+)(pt|px)', style, re.IGNORECASE)
            if size_match:
                size, unit = size_match.groups()
                size = float(size)
                if unit == 'pt':
                    is_large = size >= 18 or (is_bold and size >= 14)
                elif unit == 'px':
                    is_large = size >= 24 or (is_bold and size >= 19)
        
        return is_large
    
    def check_wcag_compliance(self, contrast_ratio: float, is_large: bool) -> Dict:
        """Check if contrast ratio meets WCAG guidelines"""
        return {
            'aa_normal': contrast_ratio >= self.WCAG_AA_NORMAL,
            'aa_large': contrast_ratio >= self.WCAG_AA_LARGE,
            'aaa_normal': contrast_ratio >= self.WCAG_AAA_NORMAL,
            'aaa_large': contrast_ratio >= self.WCAG_AAA_LARGE,
            'passes_aa': contrast_ratio >= (self.WCAG_AA_LARGE if is_large else self.WCAG_AA_NORMAL),
            'passes_aaa': contrast_ratio >= (self.WCAG_AAA_LARGE if is_large else self.WCAG_AAA_NORMAL)
        }
    
    def analyze_html(self, html_content: str) -> Dict:
        """
        Analyze HTML content for color contrast issues
        Returns analysis results with issues found
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        issues = []
        elements_checked = 0
        
        # Text elements to check
        text_elements = soup.find_all(['p', 'span', 'div', 'a', 'button', 'h1', 'h2', 
                                       'h3', 'h4', 'h5', 'h6', 'li', 'td', 'th', 'label'])
        
        for idx, element in enumerate(text_elements):
            # Skip elements without visible text
            text = element.get_text(strip=True)
            if not text:
                continue
            
            elements_checked += 1
            
            # Get colors
            colors = self.get_computed_colors(element)
            if not colors['foreground'] or not colors['background']:
                continue
            
            # Calculate contrast
            contrast_ratio = self.calculate_contrast_ratio(
                colors['foreground'], 
                colors['background']
            )
            
            # Check if large text
            is_large = self.is_large_text(element)
            
            # Check compliance
            compliance = self.check_wcag_compliance(contrast_ratio, is_large)
            
            # If it fails AA, it's an issue
            if not compliance['passes_aa']:
                issue = {
                    'element': element.name,
                    'text_preview': text[:100] if len(text) > 100 else text,
                    'foreground_color': self.rgb_to_hex(colors['foreground']),
                    'background_color': self.rgb_to_hex(colors['background']),
                    'contrast_ratio': round(contrast_ratio, 2),
                    'is_large_text': is_large,
                    'required_ratio': self.WCAG_AA_LARGE if is_large else self.WCAG_AA_NORMAL,
                    'compliance': compliance,
                    'severity': 'high' if contrast_ratio < 3.0 else 'medium',
                    'xpath': self._get_xpath(element),
                    'element_index': idx
                }
                issues.append(issue)
        
        return {
            'total_elements_checked': elements_checked,
            'total_issues_found': len(issues),
            'issues': issues,
            'summary': {
                'high_severity': len([i for i in issues if i['severity'] == 'high']),
                'medium_severity': len([i for i in issues if i['severity'] == 'medium'])
            }
        }
    
    @staticmethod
    def _get_xpath(element) -> str:
        """Generate a simple XPath-like selector for an element"""
        components = []
        child = element
        
        for parent in child.parents:
            siblings = parent.find_all(child.name, recursive=False)
            components.append(
                child.name if len(siblings) == 1
                else f"{child.name}[{siblings.index(child) + 1}]"
            )
            child = parent
            if len(components) >= 5:  # Limit depth
                break
        
        components.reverse()
        return '/' + '/'.join(components) if components else f'/{element.name}'
    
    def add_tooltips_to_html(self, html_content: str, issues: List[Dict]) -> str:
        """
        Add tooltip markers to HTML where contrast issues exist
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Add styles for tooltips
        style_tag = soup.new_tag('style')
        style_tag.string = """
        .contrast-issue-marker {
            border: 2px solid red !important;
            position: relative;
            cursor: help;
        }
        .contrast-issue-marker::after {
            content: '⚠️';
            position: absolute;
            top: -10px;
            right: -10px;
            background: red;
            color: white;
            border-radius: 50%;
            width: 20px;
            height: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
        }
        .contrast-tooltip {
            visibility: hidden;
            background-color: #333;
            color: #fff;
            text-align: left;
            border-radius: 6px;
            padding: 10px;
            position: absolute;
            z-index: 10000;
            bottom: 125%;
            left: 50%;
            transform: translateX(-50%);
            width: 300px;
            font-size: 12px;
            line-height: 1.4;
        }
        .contrast-issue-marker:hover .contrast-tooltip {
            visibility: visible;
        }
        """
        
        if soup.head:
            soup.head.append(style_tag)
        else:
            head = soup.new_tag('head')
            head.append(style_tag)
            soup.insert(0, head)
        
        # Find all text elements again and mark issues
        text_elements = soup.find_all(['p', 'span', 'div', 'a', 'button', 'h1', 'h2', 
                                       'h3', 'h4', 'h5', 'h6', 'li', 'td', 'th', 'label'])
        
        for idx, element in enumerate(text_elements):
            # Find if this element has an issue
            matching_issues = [i for i in issues if i['element_index'] == idx]
            
            if matching_issues:
                issue = matching_issues[0]
                
                # Add marker class
                element['class'] = element.get('class', []) + ['contrast-issue-marker']
                element['data-contrast-issue'] = 'true'
                
                # Create tooltip
                tooltip = soup.new_tag('div')
                tooltip['class'] = 'contrast-tooltip'
                tooltip.string = f"""
Contrast Issue!
Ratio: {issue['contrast_ratio']}:1
Required: {issue['required_ratio']}:1
Foreground: {issue['foreground_color']}
Background: {issue['background_color']}
Severity: {issue['severity'].upper()}
                """.strip()
                
                element.append(tooltip)
        
        return str(soup)
