# ColorSense - Color Contrast Analyzer

## Overview

ColorSense is a color contrast analysis tool that checks web pages for WCAG 2.1 compliance. It identifies text elements with insufficient contrast ratios and can mark them with visual tooltips.

## Features

- ✅ **WCAG 2.1 Compliance Checking**: Validates against AA and AAA standards
- ✅ **Automated Analysis**: Scans all text elements in HTML
- ✅ **Visual Markers**: Optionally adds tooltips to problematic elements
- ✅ **Detailed Reporting**: Provides contrast ratios, color values, and severity levels
- ✅ **Large Text Detection**: Distinguishes between normal and large text requirements

## WCAG Standards

### Level AA (Minimum)
- **Normal text**: 4.5:1 contrast ratio
- **Large text** (18pt+ or 14pt+ bold): 3:1 contrast ratio

### Level AAA (Enhanced)
- **Normal text**: 7:1 contrast ratio
- **Large text**: 4.5:1 contrast ratio

## API Endpoints

### POST `/colorsense/analyze-contrast/`

Analyzes a webpage for color contrast issues by fetching from a URL.

#### Request Body

```json
{
  "url": "https://example.com",
  "add_tooltips": false
}
```

**Parameters:**
- `url` (required): The URL of the webpage to analyze
- `add_tooltips` (optional): Whether to return HTML with visual markers (default: false)

---

### POST `/colorsense/analyze-html/` ⚡ **FASTER**

Analyzes HTML content provided directly by the user. **This endpoint is faster** as it doesn't need to fetch content from a URL.

#### Request Body

```json
{
  "html": "<html><body>...</body></html>",
  "add_tooltips": false
}
```

**Parameters:**
- `html` (required): The HTML content to analyze
- `add_tooltips` (optional): Whether to return HTML with visual markers (default: false)

#### Response (Both Endpoints)

```json
{
  "url": "https://example.com",
  "analysis": {
    "total_elements_checked": 45,
    "total_issues_found": 8,
    "summary": {
      "high_severity": 3,
      "medium_severity": 5
    },
    "issues": [
      {
        "element": "p",
        "text_preview": "This is some text with poor contrast",
        "foreground_color": "#777777",
        "background_color": "#ffffff",
        "contrast_ratio": 4.47,
        "is_large_text": false,
        "required_ratio": 4.5,
        "compliance": {
          "aa_normal": false,
          "aa_large": true,
          "aaa_normal": false,
          "aaa_large": false,
          "passes_aa": false,
          "passes_aaa": false
        },
        "severity": "medium",
        "xpath": "/body/div[1]/p[2]",
        "element_index": 5
      }
    ]
  },
  "marked_html": "<!-- Only included if add_tooltips=true -->"
}
```

#### Response Fields

- **total_elements_checked**: Number of text elements analyzed
- **total_issues_found**: Number of contrast violations found
- **summary**: Breakdown by severity level
  - `high_severity`: Contrast ratio < 3.0
  - `medium_severity`: Contrast ratio >= 3.0 but fails AA
- **issues**: Array of contrast violations
  - `element`: HTML element tag name
  - `text_preview`: First 100 characters of element text
  - `foreground_color`: Text color in hex format
  - `background_color`: Background color in hex format
  - `contrast_ratio`: Calculated contrast ratio (1-21)
  - `is_large_text`: Whether text qualifies as large
  - `required_ratio`: Minimum ratio needed for AA compliance
  - `compliance`: Object showing which standards are met
  - `severity`: Issue severity (high/medium)
  - `xpath`: Element location in DOM
  - `element_index`: Internal reference for tooltip marking

## How It Works

### 1. Color Extraction
The analyzer extracts colors from:
- Inline styles (color, background-color, background)
- Common color formats (hex, rgb, rgba, named colors)

### 2. Contrast Calculation
Uses the WCAG formula:
```
Contrast Ratio = (L1 + 0.05) / (L2 + 0.05)
```
Where L1 and L2 are relative luminance values.

### 3. Relative Luminance
Calculated per WCAG specification:
```
L = 0.2126 * R + 0.7152 * G + 0.0722 * B
```
With gamma correction applied to RGB channels.

### 4. Compliance Checking
Compares calculated ratios against WCAG thresholds based on text size and weight.

### 5. Tooltip Generation (Optional)
When `add_tooltips=true`, the analyzer:
- Adds CSS styles for visual markers
- Wraps problematic elements with warning indicators
- Includes hover tooltips with issue details

## Color Formats Supported

- **Hex**: `#ffffff`, `#fff`
- **RGB**: `rgb(255, 255, 255)`
- **RGBA**: `rgba(255, 255, 255, 0.5)` (alpha ignored)
- **Named**: `white`, `black`, `red`, etc.

## Element Detection

### Text Elements Analyzed
- Paragraphs (`<p>`)
- Spans (`<span>`)
- Divs with text (`<div>`)
- Links (`<a>`)
- Buttons (`<button>`)
- Headings (`<h1>`-`<h6>`)
- List items (`<li>`)
- Table cells (`<td>`, `<th>`)
- Labels (`<label>`)

### Large Text Detection
Text is considered "large" if:
- Element is `<h1>`, `<h2>`, or `<h3>`, OR
- Font size is 18pt+ (24px+), OR
- Font size is 14pt+ (19px+) AND font-weight is bold (700+)

## Example Usage

### Basic Analysis (URL)

```bash
curl -X POST "http://localhost:8000/colorsense/analyze-contrast/" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

### Basic Analysis (HTML) - Faster ⚡

```bash
curl -X POST "http://localhost:8000/colorsense/analyze-html/" \
  -H "Content-Type: application/json" \
  -d '{
    "html": "<html><body style=\"color: #ccc; background: #fff;\"><p>Low contrast text</p></body></html>",
    "add_tooltips": false
  }'
```

### With Tooltips (URL)

```bash
curl -X POST "http://localhost:8000/colorsense/analyze-contrast/" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "add_tooltips": true}'
```

### With Tooltips (HTML) - Faster ⚡

```bash
curl -X POST "http://localhost:8000/colorsense/analyze-html/" \
  -H "Content-Type: application/json" \
  -d '{
    "html": "<html><body style=\"color: #ccc; background: #fff;\"><p>Low contrast text</p></body></html>",
    "add_tooltips": true
  }'
```

### Python Example (URL)

```python
import requests

response = requests.post(
    "http://localhost:8000/colorsense/analyze-contrast/",
    json={
        "url": "https://example.com",
        "add_tooltips": False
    }
)

data = response.json()
print(f"Found {data['analysis']['total_issues_found']} contrast issues")

for issue in data['analysis']['issues']:
    print(f"- {issue['element']}: {issue['contrast_ratio']}:1 (needs {issue['required_ratio']}:1)")
```

### Python Example (HTML) - Faster ⚡

```python
import requests

html_content = """
<html>
<body>
    <p style="color: #777; background: #fff;">Medium contrast</p>
    <p style="color: #ccc; background: #fff;">Low contrast</p>
</body>
</html>
"""

response = requests.post(
    "http://localhost:8000/colorsense/analyze-html/",
    json={
        "html": html_content,
        "add_tooltips": True
    }
)

data = response.json()
print(f"Found {data['analysis']['total_issues_found']} contrast issues")

# Save marked HTML if tooltips were requested
if 'marked_html' in data:
    with open('marked_output.html', 'w') as f:
        f.write(data['marked_html'])
    print("Marked HTML saved to marked_output.html")
```

## Limitations

1. **Static Analysis Only**: Only analyzes inline styles and default colors
2. **No CSS File Parsing**: External stylesheets are not analyzed
3. **No JavaScript Execution**: Dynamic color changes are not detected
4. **Alpha Channel**: Transparency is not fully accounted for
5. **Inherited Styles**: Limited inheritance tracking from parent elements

## Best Practices

1. Use with rendered pages for more accurate results
2. Combine with manual testing for comprehensive coverage
3. Check results against actual rendered colors
4. Consider different color modes (light/dark themes)
5. Test with real assistive technologies

## Related Tools

- **AltSense**: Alt text analysis
- **LinkSense**: Link accessibility checking
- **GeminiSense**: AI-powered accessibility suggestions

## References

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Understanding Contrast Ratios](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html)
- [Color Contrast Checker](https://webaim.org/resources/contrastchecker/)
