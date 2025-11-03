"""
Anchor Text Accessibility ML Module

This module provides machine learning capabilities for evaluating
anchor text accessibility for screen readers.

Main functions:
- predict_anchor_text(text): Get detailed prediction for anchor text
- is_anchor_text_accessible(text): Simple boolean check
- predict_batch(texts): Batch predictions for multiple texts
"""

from .predict import (
    predict_anchor_text,
    is_anchor_text_accessible,
    predict_batch,
    AnchorTextClassifier,
    get_classifier
)

__all__ = [
    'predict_anchor_text',
    'is_anchor_text_accessible', 
    'predict_batch',
    'AnchorTextClassifier',
    'get_classifier'
]

__version__ = '1.0.0'
