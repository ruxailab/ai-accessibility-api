# Quick Start Guide - Image Alt Text Generator

## Overview

AI-powered image captioning that automatically generates descriptive alt text for images using the BLIP pretrained vision model.

**Input**: Image (URL or file)  
**Output**: Descriptive text suitable for alt attributes

## What's Been Created

```
ML_vision/
├── image_captioner.py         # Core BLIP model integration
├── predict.py                  # High-level prediction API
├── demo.py                     # Usage examples
├── __init__.py                 # Module initialization
├── README.md                   # Full documentation
└── QUICKSTART.md              # This file
```

## Quick Setup

### 1. Install Dependencies

```bash
pip install transformers torch pillow requests
```

**Required packages:**
- `transformers` - Hugging Face library for pretrained models
- `torch` - PyTorch deep learning framework
- `pillow` - Image processing
- `requests` - HTTP requests for downloading images

### 2. First Run

On first use, the BLIP model (~990MB) will download automatically:

```python
from ML_vision import predict_alt_text_from_url

# This will download the model on first run (one-time, ~5 min)
result = predict_alt_text_from_url("https://example.com/image.jpg")
print(result['alt_text'])
```

### 3. Test It

```bash
cd ML_vision
python demo.py
```

## Simple Usage

### Method 1: From URL

```python
from ML_vision import predict_alt_text_from_url

result = predict_alt_text_from_url("https://example.com/cat.jpg")

if result['success']:
    print(result['alt_text'])
    # Output: "a cat sitting on a couch"
```

### Method 2: From File

```python
from ML_vision import predict_alt_text_from_file

result = predict_alt_text_from_file("/path/to/image.jpg")
print(result['alt_text'])
```

### Method 3: For IMG Tags

```python
from ML_vision import suggest_alt_text_for_img_tag

# Works with URL or file path
suggestion = suggest_alt_text_for_img_tag("https://example.com/photo.jpg")

print(f"<img src='...' alt='{suggestion['suggested_alt']}'>")
```

### Method 4: Batch Processing

```python
from ML_vision import batch_predict_alt_text

images = [
    "https://example.com/image1.jpg",
    "https://example.com/image2.jpg",
    "/local/image3.jpg"
]

results = batch_predict_alt_text(images)

for r in results:
    if r['success']:
        print(f"{r['src']}: {r['suggested_alt']}")
```

## Integration with AltSense

### Quick Integration

Add to `app/lib/altsenelib.py`:

```python
from ML_vision import suggest_alt_text_for_img_tag

def analyze_image_tag(tag):
    issues = []
    
    # ... existing checks ...
    
    # Add ML suggestion for missing/vague alt
    if is_alt_missing(tag) or is_alt_vague(tag):
        img_src = tag.get('src', '')
        if img_src:
            try:
                suggestion = suggest_alt_text_for_img_tag(img_src)
                if suggestion['success']:
                    issues.append({
                        "module": "imagealt-ML",
                        "element": str(tag),
                        "issue": "Missing or vague alt text",
                        "help": f"ML suggests: '{suggestion['suggested_alt']}'",
                        "ml_suggestion": suggestion['suggested_alt']
                    })
            except Exception as e:
                # Handle gracefully
                pass
    
    return issues
```

### API Endpoint

Add to `app/routes/altsense.py`:

```python
from fastapi import APIRouter
from pydantic import BaseModel
from ML_vision import predict_alt_text_from_url

class ImageInput(BaseModel):
    image_url: str

@router.post("/ml-generate-alt-text/")
async def generate_alt_text_ml(input_data: ImageInput):
    """Generate alt text suggestion using ML"""
    result = predict_alt_text_from_url(input_data.image_url)
    return result
```

Test it:
```bash
curl -X POST "http://localhost:8000/altsense/ml-generate-alt-text/" \
  -H "Content-Type: application/json" \
  -d '{"image_url": "https://example.com/image.jpg"}'
```

## Response Format

All functions return a dictionary:

```python
{
    'image_url': 'https://example.com/image.jpg',  # or 'image_path'
    'alt_text': 'a cat sitting on a couch',
    'success': True,
    'method': 'standard'  # or 'detailed'
}
```

On error:
```python
{
    'image_url': 'https://example.com/broken.jpg',
    'alt_text': None,
    'success': False,
    'error': 'Failed to load image: 404'
}
```

## Configuration Options

### Standard vs Detailed

```python
# Standard (shorter, faster)
result = predict_alt_text_from_url(url, detailed=False)
# "a cat on a couch"

# Detailed (longer, more descriptive)
result = predict_alt_text_from_url(url, detailed=True)
# "a photograph of an orange cat sitting on a gray couch in a living room"
```

### Custom Model

```python
from ML_vision.image_captioner import ImageCaptioner

# Use larger model for better quality (slower, more memory)
captioner = ImageCaptioner(
    model_name="Salesforce/blip-image-captioning-large"
)

caption = captioner.generate_caption("image.jpg")
```

## Performance

| Operation | Time (CPU) | Time (GPU) |
|-----------|------------|------------|
| Model Load (first time) | 30-60s | 10-20s |
| Single Image | 2-5s | 0.5-1s |
| Batch (10 images) | 20-50s | 5-10s |

**Memory Usage:**
- Model: ~1GB RAM
- Per image: ~100-500MB

## Supported Formats

- ✅ JPEG (.jpg, .jpeg)
- ✅ PNG (.png)
- ✅ GIF (.gif)
- ✅ BMP (.bmp)
- ✅ WebP (.webp)

## Example Outputs

| Image Type | Generated Alt Text |
|------------|-------------------|
| Cat photo | "a cat sitting on a couch" |
| Person hiking | "a person walking on a trail" |
| Coffee | "a cup of coffee on a table" |
| Laptop | "a laptop computer on a desk" |
| Sunset | "the sun setting over the ocean" |

## Troubleshooting

### Issue: Dependencies Not Found
```bash
pip install transformers torch pillow requests
```

### Issue: Model Download Fails
Check internet connection. Model caches to:
- Linux/Mac: `~/.cache/huggingface/`
- Windows: `C:\Users\<user>\.cache\huggingface\`

### Issue: Out of Memory
```python
# Use CPU mode (slower but less memory)
import torch
torch.set_num_threads(1)
```

### Issue: Slow Performance
- Use GPU if available
- Use base model instead of large
- Reduce batch size
- Cache results for repeated images

## Best Practices

### ✅ Do's
- Review ML suggestions before using
- Use for missing alt text
- Batch process multiple images
- Cache results to avoid re-processing
- Test with diverse images

### ❌ Don'ts
- Don't blindly trust ML output
- Don't use for decorative images (use `alt=""`)
- Don't forget page context
- Don't overload with too many concurrent requests

## Next Steps

1. ✅ Module is created and ready
2. Install dependencies: `pip install transformers torch pillow requests`
3. Test with demo: `python demo.py`
4. Integrate into AltSense
5. Add API endpoint
6. Deploy and monitor

## Quick Reference

```python
# Simple usage
from ML_vision import predict_alt_text_from_url
result = predict_alt_text_from_url("https://example.com/image.jpg")
print(result['alt_text'])

# For img tags
from ML_vision import suggest_alt_text_for_img_tag
suggestion = suggest_alt_text_for_img_tag(img_src)
print(suggestion['suggested_alt'])

# Batch processing
from ML_vision import batch_predict_alt_text
results = batch_predict_alt_text([url1, url2, url3])

# Evaluate existing alt
from ML_vision import is_alt_text_adequate
check = is_alt_text_adequate("current alt", img_src)
print(check['is_adequate'])
```

---

**For detailed documentation**, see `ML_vision/README.md`

**Having issues?** Check the troubleshooting section or open an issue.
