# Quick Start Guide - Anchor Text ML Model

## Overview

A simple machine learning model that evaluates whether anchor text (link text) is accessible for screen readers. The model classifies text as "good" or "bad" based on descriptiveness.

## What's Been Created

```
ML/
├── training_data.csv              # 298 labeled examples
├── train_model.py                 # Training script
├── predict.py                     # Prediction module
├── anchor_text_classifier.pkl     # Trained model (63% accuracy)
├── demo.py                        # Usage examples
├── __init__.py                    # Module initialization
└── README.md                      # Full documentation
```

## Quick Test

```bash
cd ML
python demo.py
```

This will show various ways to use the model.

## How to Use in Your Code

### Method 1: Simple Boolean Check
```python
from ML.predict import is_anchor_text_accessible

# Returns True/False
is_good = is_anchor_text_accessible("click here")  # False
is_good = is_anchor_text_accessible("Download the user guide")  # True
```

### Method 2: Detailed Prediction
```python
from ML.predict import predict_anchor_text

result = predict_anchor_text("read more")
print(result)
# {
#     'text': 'read more',
#     'prediction': 'bad',
#     'confidence': 0.64,
#     'is_accessible': False,
#     'probability_good': 0.36,
#     'probability_bad': 0.64
# }
```

### Method 3: Batch Processing
```python
from ML.predict import predict_batch

texts = ["click here", "Download guide", "more info"]
results = predict_batch(texts)
```

## Integration with LinkSense

Add ML-powered checking to your existing anchor tag analyzer:

```python
# In app/lib/anchorsense.py
from ML.predict import predict_anchor_text

def analyze_anchor_tag(tag):
    issues = []
    link_text = tag.get_text(strip=True)
    
    # Use ML model
    ml_result = predict_anchor_text(link_text)
    
    if not ml_result['is_accessible']:
        issues.append({
            "code": 5,
            "module": "anchorInsight-ML",
            "element": get_pa11y_style_context(tag),
            "issue": f"ML detected non-accessible text (confidence: {ml_result['confidence']:.1%})",
            "help": "Use descriptive link text that explains the destination.",
            "ml_confidence": ml_result['confidence']
        })
    
    # ... rest of existing checks
    return issues
```

## Training Data Format

The model was trained on a CSV file with two columns:

```csv
text,label
click here,bad
Download accessibility guide,good
read more,bad
Contact support team,good
```

- **Bad examples**: Generic, non-descriptive ("click here", "read more", "here")
- **Good examples**: Descriptive, contextual ("Download the user manual", "Contact support")

## Model Performance

- **Accuracy**: ~63%
- **Training data**: 298 examples (169 bad, 129 good)
- **Algorithm**: TF-IDF + Logistic Regression
- **Model size**: ~100KB

### Example Predictions:
- ❌ "click here" → BAD (72% confidence)
- ❌ "read more" → BAD (64% confidence)  
- ❌ "here" → BAD (75% confidence)
- ✅ "Download the user guide" → GOOD (56% confidence)
- ✅ "Contact support team" → GOOD (56% confidence)

## Improving the Model

### Add More Training Data
1. Edit `ML/training_data.csv`
2. Add new examples (keep balanced)
3. Run: `python train_model.py`

### Tips for Better Data:
- Include edge cases and borderline examples
- Add domain-specific terminology
- Maintain balance between good/bad examples
- Add variations of common patterns

## Files Explained

| File | Purpose |
|------|---------|
| `training_data.csv` | Labeled examples for training |
| `train_model.py` | Trains and saves the model |
| `predict.py` | Loads model and makes predictions |
| `anchor_text_classifier.pkl` | The trained model file |
| `demo.py` | Usage examples |
| `README.md` | Full documentation |

## Common Issues

**Q: Model file not found error?**
A: Run `python train_model.py` first to create the .pkl file

**Q: Import errors?**
A: Install dependencies: `pip install scikit-learn pandas`

**Q: Low accuracy?**
A: Add more diverse training examples and retrain

**Q: False positives/negatives?**
A: Adjust confidence threshold or add more training data

## Next Steps

1. ✅ Model is trained and ready to use
2. Test it with: `python demo.py`
3. Integrate into linksense analyzer
4. Add more training data over time to improve accuracy
5. Monitor predictions and retrain as needed

## Example API Endpoint

You can add an ML-powered endpoint:

```python
# In app/routes/linksense.py
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class AnchorTextInput(BaseModel):
    text: str

@router.post("/ml-check-anchor-text/")
async def check_anchor_text_ml(input_data: AnchorTextInput):
    from ML.predict import predict_anchor_text
    result = predict_anchor_text(input_data.text)
    return result
```

Then test it:
```bash
curl -X POST "http://localhost:8000/linksense/ml-check-anchor-text/" \
  -H "Content-Type: application/json" \
  -d '{"text": "click here"}'
```

---

**For full documentation**, see `ML/README.md`
