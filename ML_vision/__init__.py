"""
ML Vision Module for Image Alt Text Generation

This module provides AI-powered image captioning to automatically
generate descriptive alt text for images using pretrained models.
"""

from .predict import (
    predict_alt_text_from_url,
    predict_alt_text_from_file,
    suggest_alt_text_for_img_tag,
    batch_predict_alt_text,
    is_alt_text_adequate
)

from .image_captioner import (
    ImageCaptioner,
    get_captioner,
    generate_alt_text,
    generate_alt_text_batch
)

__all__ = [
    # High-level prediction functions
    'predict_alt_text_from_url',
    'predict_alt_text_from_file',
    'suggest_alt_text_for_img_tag',
    'batch_predict_alt_text',
    'is_alt_text_adequate',
    
    # Low-level captioner functions
    'ImageCaptioner',
    'get_captioner',
    'generate_alt_text',
    'generate_alt_text_batch'
]

__version__ = '1.0.0'
