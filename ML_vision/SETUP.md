# ML Vision Module - Setup Instructions

## Overview

The `ML_vision` module has been created for generating alt text from images using AI. All code files are ready, but dependencies need to be installed before use.

## What's Ready

✅ **Core Module** (`image_captioner.py`)
- BLIP model integration
- Support for URLs and local files
- Standard and detailed caption modes

✅ **Prediction API** (`predict.py`)
- `predict_alt_text_from_url(url)` - Generate from URL
- `predict_alt_text_from_file(path)` - Generate from file
- `suggest_alt_text_for_img_tag(src)` - For HTML img tags
- `batch_predict_alt_text(images)` - Process multiple images

✅ **Documentation**
- `README.md` - Complete documentation
- `QUICKSTART.md` - Quick reference
- `demo.py` - Usage examples

✅ **Dependencies Added** to `requirements.txt`:
- transformers>=4.25.0
- torch>=2.0.0
- pillow>=9.0.0

## Installation Steps

### 1. Install Vision Dependencies

```bash
pip install transformers torch pillow
```

**Note**: This will download ~2-3GB of packages. PyTorch is large!

### 2. First Run (Downloads Model)

On first use, the BLIP model (~990MB) downloads automatically:

```bash
cd ML_vision
python -c "from predict import predict_alt_text_from_url; print('Model ready!')"
```

This takes 2-10 minutes depending on your internet speed.

### 3. Test It

```python
from ML_vision import predict_alt_text_from_url

result = predict_alt_text_from_url("https://images.unsplash.com/photo-1518791841217-8f162f1e1131")
print(result['alt_text'])
# Expected: "a cat sitting on a couch" or similar
```

## Quick Usage Examples

### Example 1: Simple Alt Text Generation

```python
from ML_vision import predict_alt_text_from_url

# Generate alt text from URL
result = predict_alt_text_from_url("https://example.com/image.jpg")

if result['success']:
    print(f"Alt text: {result['alt_text']}")
else:
    print(f"Error: {result['error']}")
```

### Example 2: Integration with AltSense

```python
# In app/lib/altsenelib.py
from ML_vision import suggest_alt_text_for_img_tag

def analyze_image_tag(tag):
    issues = []
    
    # Existing checks...
    if is_alt_missing(tag) or is_alt_vague(tag):
        img_src = tag.get('src', '')
        if img_src and img_src.startswith('http'):
            # Generate ML suggestion
            suggestion = suggest_alt_text_for_img_tag(img_src)
            
            if suggestion['success']:
                issues.append({
                    "module": "imagealt-ML",
                    "element": str(tag),
                    "issue": "Missing or vague alt text",
                    "help": f"AI suggests: '{suggestion['suggested_alt']}'",
                    "ml_suggestion": suggestion['suggested_alt']
                })
    
    return issues
```

### Example 3: API Endpoint

```python
# Add to app/routes/altsense.py
from fastapi import APIRouter
from pydantic import BaseModel
from ML_vision import predict_alt_text_from_url

class ImageURLInput(BaseModel):
    image_url: str

@router.post("/ml-suggest-alt-text/")
async def ml_suggest_alt_text(input_data: ImageURLInput):
    """
    Generate alt text suggestion using AI vision model
    """
    result = predict_alt_text_from_url(input_data.image_url)
    return result
```

Then include in `main.py` and test:
```bash
curl -X POST "http://localhost:8000/altsense/ml-suggest-alt-text/" \
  -H "Content-Type: application/json" \
  -d '{"image_url": "https://example.com/image.jpg"}'
```

## System Requirements

### Minimum:
- **RAM**: 2GB free
- **Disk**: 3GB free (for model + packages)
- **Python**: 3.8+

### Recommended:
- **RAM**: 4GB+ free
- **GPU**: CUDA-capable GPU for faster processing
- **Disk**: 5GB free

## Performance

| Hardware | Single Image | 10 Images |
|----------|--------------|-----------|
| **CPU Only** | 2-5 seconds | 20-50 seconds |
| **GPU (CUDA)** | 0.5-1 second | 5-10 seconds |

## Model Details

**BLIP (Bootstrapping Language-Image Pre-training)**
- Developer: Salesforce Research
- Size: ~990MB
- Quality: State-of-the-art image captioning
- Languages: Primarily English

## File Structure

```
ML_vision/
├── image_captioner.py     # Core BLIP model wrapper
├── predict.py              # High-level prediction functions
├── demo.py                 # Usage demonstrations
├── __init__.py             # Module exports
├── README.md               # Full documentation
├── QUICKSTART.md           # Quick start guide
└── SETUP.md                # This file
```

## Available Functions

### From `predict.py`:

```python
# URL-based
predict_alt_text_from_url(image_url, detailed=False)

# File-based
predict_alt_text_from_file(image_path, detailed=False)

# For img tags
suggest_alt_text_for_img_tag(img_tag_src, detailed=False)

# Batch processing
batch_predict_alt_text(image_sources, detailed=False)

# Evaluation
is_alt_text_adequate(current_alt, image_source, threshold=0.7)
```

### From `image_captioner.py`:

```python
# Direct model access
from ML_vision.image_captioner import ImageCaptioner

captioner = ImageCaptioner()
caption = captioner.generate_caption("image.jpg")
detailed = captioner.generate_detailed_caption("image.jpg")
```

## Troubleshooting

### Issue: "No module named 'PIL'"
```bash
pip install pillow
```

### Issue: "No module named 'transformers'"
```bash
pip install transformers torch
```

### Issue: "CUDA out of memory"
Model will automatically fall back to CPU mode.

### Issue: Model download fails
Check internet connection. Model caches to `~/.cache/huggingface/`

### Issue: Slow performance
- Use GPU if available
- Process images in batches
- Use standard (not detailed) mode
- Cache results for repeated images

## Next Steps

1. ✅ Module code is ready
2. ⏳ Install dependencies: `pip install transformers torch pillow`
3. ⏳ Test basic functionality
4. ⏳ Integrate with AltSense
5. ⏳ Add API endpoint
6. ⏳ Deploy and test

## Optional: Pre-download Model

To download the model without running predictions:

```bash
python -c "from transformers import BlipProcessor, BlipForConditionalGeneration; BlipProcessor.from_pretrained('Salesforce/blip-image-captioning-base'); BlipForConditionalGeneration.from_pretrained('Salesforce/blip-image-captioning-base')"
```

## Important Notes

⚠️ **Model Size**: The pretrained model is ~990MB. Make sure you have enough disk space and a stable internet connection for the first download.

⚠️ **Processing Time**: Image captioning is computationally intensive. First image takes longer as the model loads into memory.

⚠️ **Accuracy**: ML-generated captions are suggestions. Always review them for accuracy and context appropriateness.

⚠️ **Privacy**: Images are processed locally. No data is sent to external servers (except for downloading the model initially).

## Support

- Full documentation: `ML_vision/README.md`
- Quick reference: `ML_vision/QUICKSTART.md`
- Examples: `ML_vision/demo.py`

---

**Ready to start?**
```bash
pip install transformers torch pillow
cd ML_vision
python demo.py
```
