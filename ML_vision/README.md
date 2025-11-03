# Image Caption Generator for Alt Text Suggestions

AI-powered image captioning to generate descriptive alt text for images using pretrained vision-language models.

## Overview

This module uses **BLIP (Bootstrapping Language-Image Pre-training)**, a state-of-the-art pretrained model from Salesforce, to automatically generate descriptive text for images. Perfect for suggesting alt text in accessibility analysis.

## Features

- 🖼️ **Image to Text**: Converts images to descriptive text
- 🌐 **URL Support**: Works with image URLs
- 📁 **File Support**: Works with local image files
- ⚡ **Fast Inference**: Uses pretrained models (no training needed)
- 🎯 **Accessibility Focused**: Generates descriptions suitable for alt text

## Installation

### Required Dependencies

```bash
pip install transformers torch pillow requests
```

Or add to `requirements.txt`:
```
transformers>=4.25.0
torch>=2.0.0
pillow>=9.0.0
requests>=2.28.0
```

### Install Dependencies

```bash
pip install transformers torch pillow requests
```

**Note**: The pretrained model (~990MB) will be downloaded automatically on first use and cached locally.

## Project Structure

```
ML_vision/
├── image_captioner.py         # Core image captioning module
├── predict.py                  # Prediction utilities
├── demo.py                     # Usage examples
├── __init__.py                 # Module initialization
└── README.md                   # This file
```

## Quick Start

### Basic Usage

```python
from ML_vision.predict import predict_alt_text_from_url

# Generate alt text from image URL
result = predict_alt_text_from_url("https://example.com/image.jpg")
print(result['alt_text'])
# Output: "a cat sitting on a couch"
```

### Integration with AltSense

```python
from ML_vision.predict import suggest_alt_text_for_img_tag

# For an img tag src attribute
img_src = "https://example.com/photo.jpg"
suggestion = suggest_alt_text_for_img_tag(img_src)

if suggestion['success']:
    print(f"Suggested alt text: {suggestion['suggested_alt']}")
else:
    print(f"Error: {suggestion['error']}")
```

## API Reference

### Main Functions

#### `predict_alt_text_from_url(image_url, detailed=False)`
Generate alt text from an image URL.

**Parameters:**
- `image_url` (str): URL of the image
- `detailed` (bool): Generate detailed description (default: False)

**Returns:** Dictionary with:
```python
{
    'image_url': str,
    'alt_text': str,
    'success': bool,
    'method': 'standard' or 'detailed'
}
```

**Example:**
```python
result = predict_alt_text_from_url("https://example.com/dog.jpg")
print(result['alt_text'])  # "a dog sitting in grass"
```

---

#### `predict_alt_text_from_file(image_path, detailed=False)`
Generate alt text from a local image file.

**Parameters:**
- `image_path` (str): Path to image file
- `detailed` (bool): Generate detailed description

**Returns:** Dictionary with prediction results

**Example:**
```python
result = predict_alt_text_from_file("/path/to/image.jpg")
print(result['alt_text'])
```

---

#### `suggest_alt_text_for_img_tag(img_tag_src, detailed=False)`
Suggest alt text for an img tag based on its src attribute.

**Parameters:**
- `img_tag_src` (str): The src attribute value (URL or path)
- `detailed` (bool): Generate detailed description

**Returns:**
```python
{
    'src': str,
    'suggested_alt': str,
    'success': bool,
    'error': str (if failed)
}
```

**Example:**
```python
suggestion = suggest_alt_text_for_img_tag("https://example.com/cat.jpg")
if suggestion['success']:
    print(f"Use this alt text: {suggestion['suggested_alt']}")
```

---

#### `batch_predict_alt_text(image_sources, detailed=False)`
Generate alt text for multiple images.

**Parameters:**
- `image_sources` (List[str]): List of image URLs or paths
- `detailed` (bool): Generate detailed descriptions

**Returns:** List of prediction dictionaries

**Example:**
```python
images = [
    "https://example.com/image1.jpg",
    "https://example.com/image2.jpg"
]
results = batch_predict_alt_text(images)
for r in results:
    print(f"{r['src']}: {r['suggested_alt']}")
```

---

### Advanced Usage

#### Using the Image Captioner Directly

```python
from ML_vision.image_captioner import ImageCaptioner

# Initialize captioner
captioner = ImageCaptioner()

# Generate caption
caption = captioner.generate_caption("https://example.com/image.jpg")
print(caption)

# Generate detailed caption with prompt
detailed = captioner.generate_detailed_caption(
    "https://example.com/image.jpg",
    prompt="a photograph of"
)
print(detailed)
```

#### Custom Model

```python
from ML_vision.image_captioner import ImageCaptioner

# Use larger model for better quality (but slower)
captioner = ImageCaptioner(
    model_name="Salesforce/blip-image-captioning-large"
)

caption = captioner.generate_caption("image.jpg")
```

## Integration Examples

### Example 1: Enhance AltSense Analysis

```python
# In app/lib/altsenelib.py
from ML_vision.predict import suggest_alt_text_for_img_tag

def analyze_image_tag(tag):
    issues = []
    
    # Existing checks...
    if is_alt_missing(tag) or is_alt_vague(tag):
        # Get ML suggestion
        img_src = tag.get('src', '')
        if img_src:
            suggestion = suggest_alt_text_for_img_tag(img_src)
            
            if suggestion['success']:
                issues.append({
                    "module": "imagealt-ML",
                    "element": str(tag),
                    "issue": "Missing or vague alt text",
                    "help": f"ML suggests: '{suggestion['suggested_alt']}'",
                    "ml_suggestion": suggestion['suggested_alt']
                })
    
    return issues
```

### Example 2: API Endpoint

```python
# In app/routes/altsense.py
from fastapi import APIRouter
from pydantic import BaseModel
from ML_vision.predict import predict_alt_text_from_url

router = APIRouter()

class ImageURLInput(BaseModel):
    image_url: str
    detailed: bool = False

@router.post("/generate-alt-text/")
async def generate_alt_text_endpoint(input_data: ImageURLInput):
    """
    Generate alt text suggestion for an image
    """
    result = predict_alt_text_from_url(
        input_data.image_url,
        detailed=input_data.detailed
    )
    return result
```

### Example 3: Batch Processing

```python
from ML_vision.predict import batch_predict_alt_text
from bs4 import BeautifulSoup

def suggest_alt_text_for_webpage(html_content):
    """Extract all images and suggest alt text"""
    soup = BeautifulSoup(html_content, 'html.parser')
    img_tags = soup.find_all('img')
    
    # Get all image sources
    image_srcs = [img.get('src') for img in img_tags if img.get('src')]
    
    # Generate alt text for all images
    suggestions = batch_predict_alt_text(image_srcs)
    
    return suggestions
```

## Model Information

### BLIP Model

- **Name**: BLIP (Bootstrapping Language-Image Pre-training)
- **Developer**: Salesforce Research
- **Size**: ~990MB (base model), ~1.9GB (large model)
- **Architecture**: Vision Transformer + Language Model
- **Training**: Pretrained on millions of image-text pairs

### Available Models

| Model | Size | Quality | Speed |
|-------|------|---------|-------|
| `Salesforce/blip-image-captioning-base` | ~990MB | Good | Fast |
| `Salesforce/blip-image-captioning-large` | ~1.9GB | Better | Slower |

### Sample Outputs

| Image | Generated Alt Text |
|-------|-------------------|
| Cat on couch | "a cat sitting on a couch" |
| Person hiking | "a person walking on a trail in the mountains" |
| Coffee cup | "a cup of coffee on a wooden table" |
| Laptop | "a laptop computer sitting on a desk" |

## Performance Considerations

### First Run
- Downloads model (~990MB) - takes 1-5 minutes depending on connection
- Model is cached locally for future use

### Inference Speed
- **CPU**: ~2-5 seconds per image
- **GPU**: ~0.5-1 second per image

### Memory Usage
- **Model**: ~1GB RAM
- **Image Processing**: ~100-500MB per batch

## Troubleshooting

### Common Issues

**1. Model Download Fails**
```
Error: Connection timeout
```
**Solution**: Check internet connection. Model will be cached after first successful download.

**2. Out of Memory**
```
RuntimeError: CUDA out of memory
```
**Solution**: Use CPU instead or reduce batch size.

**3. Image Load Error**
```
Failed to load image from URL
```
**Solution**: Ensure image URL is accessible and format is supported (JPEG, PNG, etc.).

### Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- BMP (.bmp)
- WebP (.webp)

## Best Practices

### Alt Text Generation

1. **Review ML suggestions**: Always review generated text for accuracy
2. **Context matters**: ML can't know page context - adjust as needed
3. **Decorative images**: If image is decorative, use empty alt (`alt=""`)
4. **Complex images**: May need manual description beyond ML capability

### Performance

1. **Batch processing**: Use `batch_predict_alt_text()` for multiple images
2. **Cache results**: Cache ML suggestions to avoid repeated inference
3. **Use appropriate model**: Base model is sufficient for most cases
4. **GPU acceleration**: Use GPU if available for faster processing

## Limitations

- **Context-blind**: Doesn't understand page context or purpose
- **Generic descriptions**: May produce generic captions
- **Not perfect**: May misidentify objects or miss details
- **No OCR**: Doesn't read text within images
- **English only**: Current model primarily supports English

## Future Improvements

- [ ] Add support for multilingual captions
- [ ] Implement OCR for text-heavy images
- [ ] Add context-aware captioning
- [ ] Cache frequently accessed images
- [ ] Support for SVG and vector graphics
- [ ] Custom fine-tuning for specific domains

## Examples

See `demo.py` for comprehensive usage examples:

```bash
cd ML_vision
python demo.py
```

## License

Uses pretrained BLIP model from Salesforce Research.
Model License: BSD 3-Clause

## Contributing

To improve the vision module:
1. Test with diverse images
2. Report issues with specific image types
3. Suggest improvements for alt text formatting
4. Share domain-specific use cases

---

**Questions or Issues?** Open an issue in the main repository.
