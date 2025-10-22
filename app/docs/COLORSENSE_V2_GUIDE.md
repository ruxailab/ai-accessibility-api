# ColorSense v2.0 - Axe-Core Integration

## Overview

ColorSense v2.0 is a complete rewrite using **axe-core**, the industry-standard accessibility testing engine. This provides robust, accurate color contrast detection that follows WCAG 2.1 guidelines.

## Why Axe-Core?

The previous custom implementation had limitations:
- ❌ Didn't handle CSS variables and computed styles well
- ❌ Missed edge cases in complex layouts
- ❌ Limited to inline styles only
- ❌ Required manual WCAG formula implementation

Axe-core provides:
- ✅ Industry-standard accessibility testing
- ✅ Handles computed styles, CSS variables, inheritance
- ✅ Actively maintained by Deque Systems
- ✅ Used by major companies (Microsoft, Google, etc.)
- ✅ Complete WCAG 2.1 Level AA/AAA support
- ✅ Detailed violation reports with actionable guidance

## API Endpoints

### 1. `/colorsense/examine` - URL Analysis

Analyze color contrast on any publicly accessible URL.

**Method:** POST  
**Content-Type:** application/json

**Request:**
```json
{
  "url": "https://example.com",
  "add_markers": true
}
```

**Response:**
```json
{
  "url": "https://example.com",
  "violations": [
    {
      "rule_id": "color-contrast",
      "description": "Elements must have sufficient color contrast",
      "help": "Ensures the contrast between foreground and background colors meets WCAG 2 AA contrast ratio thresholds",
      "help_url": "https://dequeuniversity.com/rules/axe/4.4/color-contrast",
      "impact": "serious",
      "element": {
        "html": "<p style=\"color: #ccc; background: #fff;\">Low contrast text</p>",
        "target": ["body > p:nth-child(2)"]
      },
      "failure_summary": "Fix any of the following:\n  Element has insufficient color contrast of 1.61 (foreground color: #cccccc, background color: #ffffff, font size: 12.0pt (16px), font weight: normal). Expected contrast ratio of 4.5:1",
      "message": "Element has insufficient color contrast of 1.61"
    }
  ],
  "total_issues": 1,
  "passed": false,
  "marked_html": "<!DOCTYPE html>..."
}
```

**Fields:**
- `url`: The analyzed URL
- `violations`: Array of color contrast issues found
- `total_issues`: Count of violations
- `passed`: `true` if no issues, `false` otherwise
- `marked_html`: HTML with visual markers (if `add_markers=true`)

### 2. `/colorsense/examinehtml/` - File Upload Analysis

Analyze color contrast in an HTML file. **Recommended for complex HTML** to avoid JSON escaping issues.

**Method:** POST  
**Content-Type:** multipart/form-data

**Request:**
```bash
curl -X POST "http://localhost:8000/colorsense/examinehtml/" \
  -F "file=@portfolio.html" \
  -F "add_markers=true"
```

**Response:**
```json
{
  "source": "html_content",
  "filename": "portfolio.html",
  "violations": [...],
  "total_issues": 3,
  "passed": false,
  "marked_html": "<!DOCTYPE html>..."
}
```

### 3. `/colorsense/health` - Health Check

Check if the service is running.

**Method:** GET

**Response:**
```json
{
  "status": "healthy",
  "service": "ColorSense Axe-Core Integration",
  "version": "2.0",
  "engine": "axe-core"
}
```

## Visual Markers

When `add_markers=true`, the API adds simple visual indicators to problematic elements:

- **Red outline** around elements with contrast issues
- **Tooltip** appears on hover showing the issue severity

The markers use simple CSS:
```css
.axe-contrast-issue {
    outline: 3px solid red !important;
}
.axe-contrast-tooltip {
    background: red !important;
    color: white !important;
    /* Shows on hover */
}
```

## Usage Examples

### Python Example

```python
import requests

# Test URL
response = requests.post(
    "http://localhost:8000/colorsense/examine",
    json={
        "url": "https://example.com",
        "add_markers": True
    }
)

result = response.json()
print(f"Found {result['total_issues']} contrast issues")

# Save marked HTML
if 'marked_html' in result:
    with open('output.html', 'w') as f:
        f.write(result['marked_html'])
```

### File Upload Example

```python
import requests

with open('portfolio.html', 'rb') as f:
    response = requests.post(
        "http://localhost:8000/colorsense/examinehtml/",
        files={'file': f},
        data={'add_markers': 'true'}
    )

result = response.json()

# Save marked HTML
with open('portfolio_marked.html', 'w') as f:
    f.write(result['marked_html'])
```

### cURL Examples

**URL Analysis:**
```bash
curl -X POST "http://localhost:8000/colorsense/examine" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "add_markers": true}'
```

**File Upload:**
```bash
curl -X POST "http://localhost:8000/colorsense/examinehtml/" \
  -F "file=@your-file.html" \
  -F "add_markers=true"
```

### JavaScript/Fetch Example

```javascript
// URL Analysis
const response = await fetch('http://localhost:8000/colorsense/examine', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    url: 'https://example.com',
    add_markers: true
  })
});

const result = await response.json();
console.log(`Found ${result.total_issues} issues`);

// File Upload
const formData = new FormData();
formData.append('file', htmlFile);
formData.append('add_markers', 'true');

const response = await fetch('http://localhost:8000/colorsense/examinehtml/', {
  method: 'POST',
  body: formData
});
```

## Understanding Violations

Each violation includes:

1. **rule_id**: The axe-core rule that was violated (e.g., "color-contrast")
2. **description**: Human-readable description of the issue
3. **help**: Guidance on what the rule checks
4. **help_url**: Link to detailed documentation
5. **impact**: Severity level
   - `critical`: Must fix
   - `serious`: Should fix
   - `moderate`: Should consider fixing
   - `minor`: Nice to fix
6. **element**: The problematic HTML element
7. **failure_summary**: Detailed explanation with contrast ratios
8. **message**: Short summary of the issue

## WCAG Standards

Axe-core checks against WCAG 2.1 standards:

### Level AA (Default)
- **Normal text**: Minimum contrast ratio of **4.5:1**
- **Large text** (18pt+ or 14pt+ bold): Minimum **3:1**

### Level AAA (Stricter)
- **Normal text**: Minimum contrast ratio of **7:1**
- **Large text**: Minimum **4.5:1**

## Installation

1. Install dependencies:
```bash
pip install axe-selenium-python webdriver-manager selenium
```

2. The system uses Chrome/Chromium. The webdriver-manager automatically downloads the correct ChromeDriver version.

## Testing

Run the comprehensive test suite:

```bash
python test_axe_colorsense.py
```

This tests:
1. Health check
2. URL examination
3. HTML file examination
4. Portfolio HTML (if available)

## Comparison: Old vs New

| Feature | Old (Custom) | New (Axe-Core) |
|---------|--------------|----------------|
| Detection Accuracy | ⚠️ Limited | ✅ Industry-standard |
| CSS Variables | ❌ Not supported | ✅ Fully supported |
| Computed Styles | ❌ Not supported | ✅ Fully supported |
| Maintenance | ⚠️ Manual updates | ✅ Actively maintained |
| WCAG Compliance | ⚠️ Basic | ✅ Complete 2.1 AA/AAA |
| Documentation | ⚠️ Limited | ✅ Extensive |
| False Positives | ⚠️ Possible | ✅ Minimal |
| Performance | ✅ Fast | ✅ Acceptable |

## Migration Guide

If you were using the old endpoints:

**Old:** `/colorsense/analyze-contrast/`  
**New:** `/colorsense/examine`

**Old:** `/colorsense/analyze-html-file/`  
**New:** `/colorsense/examinehtml/`

The response format is different - see API documentation above.

## Troubleshooting

### "ChromeDriver not found"
- The webdriver-manager should auto-install ChromeDriver
- Ensure you have Chrome or Chromium installed

### "Timeout errors"
- Large pages may take longer to analyze
- Increase timeout in your request (default: 60s)

### "No issues detected when there should be"
- Axe-core only detects actual rendered issues
- Ensure the HTML includes proper CSS
- Check that colors are actually applied

## Performance Notes

- URL analysis: 5-15 seconds (depends on page size)
- HTML analysis: 2-10 seconds (depends on HTML size)
- The headless browser needs time to render and compute styles

## Best Practices

1. **Use file upload for complex HTML** - Avoids JSON escaping issues
2. **Save marked HTML** - Visual inspection is valuable
3. **Check help URLs** - Axe provides excellent guidance
4. **Fix critical/serious first** - Prioritize by impact
5. **Test after fixes** - Re-run analysis to verify

## Architecture

```
Request
  ↓
FastAPI Route (axe_colorsense.py)
  ↓
Controller (axe_contrast_controller.py)
  ↓
Axe Checker Library (axe_contrast_checker.py)
  ↓
Selenium + Axe-Core
  ↓
Response with violations + marked HTML
```

## Support

For issues or questions:
1. Check the axe-core documentation: https://github.com/dequelabs/axe-core
2. Review WCAG guidelines: https://www.w3.org/WAI/WCAG21/quickref/
3. Test with the provided test suite

## License

This implementation uses:
- axe-core (Mozilla Public License 2.0)
- Selenium (Apache License 2.0)
- FastAPI (MIT License)
