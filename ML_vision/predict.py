"""
Simple Image Alt Text Predictor

This module provides simple functions to generate alt text for images.
Wrapper around the image_captioner module for easy integration.
"""

from typing import Union, Dict, List
from PIL import Image
from .image_captioner import get_captioner, generate_alt_text, generate_alt_text_batch


def predict_alt_text_from_url(image_url: str, detailed: bool = False) -> Dict:
    """
    Generate alt text for an image from URL.
    
    Args:
        image_url: URL of the image
        detailed: Whether to generate detailed description
        
    Returns:
        Dictionary with prediction results
        
    Example:
        >>> result = predict_alt_text_from_url("https://example.com/cat.jpg")
        >>> print(result['alt_text'])
        "a cat sitting on a couch"
    """
    try:
        alt_text = generate_alt_text(image_url, detailed=detailed)
        return {
            'image_url': image_url,
            'alt_text': alt_text,
            'success': True,
            'method': 'detailed' if detailed else 'standard'
        }
    except Exception as e:
        return {
            'image_url': image_url,
            'alt_text': None,
            'success': False,
            'error': str(e)
        }


def predict_alt_text_from_file(image_path: str, detailed: bool = False) -> Dict:
    """
    Generate alt text for an image from file path.
    
    Args:
        image_path: Path to the image file
        detailed: Whether to generate detailed description
        
    Returns:
        Dictionary with prediction results
    """
    try:
        alt_text = generate_alt_text(image_path, detailed=detailed)
        return {
            'image_path': image_path,
            'alt_text': alt_text,
            'success': True,
            'method': 'detailed' if detailed else 'standard'
        }
    except Exception as e:
        return {
            'image_path': image_path,
            'alt_text': None,
            'success': False,
            'error': str(e)
        }


def suggest_alt_text_for_img_tag(img_tag_src: str, detailed: bool = False) -> Dict:
    """
    Suggest alt text for an img tag based on its src attribute.
    
    Args:
        img_tag_src: The src attribute value (can be URL or relative path)
        detailed: Whether to generate detailed description
        
    Returns:
        Dictionary with suggestion
        
    Example:
        >>> result = suggest_alt_text_for_img_tag("https://example.com/photo.jpg")
        >>> print(result)
        {
            'src': 'https://example.com/photo.jpg',
            'suggested_alt': 'a person standing in a field',
            'success': True
        }
    """
    # Determine if it's a URL or file path
    if img_tag_src.startswith(('http://', 'https://', '//')):
        # Handle protocol-relative URLs
        if img_tag_src.startswith('//'):
            img_tag_src = 'https:' + img_tag_src
        result = predict_alt_text_from_url(img_tag_src, detailed=detailed)
    else:
        result = predict_alt_text_from_file(img_tag_src, detailed=detailed)
    
    # Reformat for img tag context
    return {
        'src': img_tag_src,
        'suggested_alt': result.get('alt_text'),
        'success': result['success'],
        'error': result.get('error')
    }


def batch_predict_alt_text(image_sources: List[str], detailed: bool = False) -> List[Dict]:
    """
    Generate alt text for multiple images.
    
    Args:
        image_sources: List of image URLs or file paths
        detailed: Whether to generate detailed descriptions
        
    Returns:
        List of prediction dictionaries
    """
    results = []
    for src in image_sources:
        result = suggest_alt_text_for_img_tag(src, detailed=detailed)
        results.append(result)
    return results


def is_alt_text_adequate(current_alt: str, image_source: str, threshold_similarity: float = 0.7) -> Dict:
    """
    Check if existing alt text is adequate by comparing with ML-generated description.
    
    Args:
        current_alt: Current alt text
        image_source: Image URL or path
        threshold_similarity: Similarity threshold (0-1)
        
    Returns:
        Dictionary with assessment
        
    Note:
        This is a simple implementation. For production, you'd want to use
        semantic similarity metrics (e.g., sentence-transformers).
    """
    try:
        # Generate ML caption
        ml_caption = generate_alt_text(image_source)
        
        # Simple word overlap similarity (basic implementation)
        current_words = set(current_alt.lower().split())
        ml_words = set(ml_caption.lower().split())
        
        if len(current_words) == 0 or len(ml_words) == 0:
            similarity = 0.0
        else:
            overlap = len(current_words & ml_words)
            similarity = overlap / max(len(current_words), len(ml_words))
        
        is_adequate = similarity >= threshold_similarity
        
        return {
            'current_alt': current_alt,
            'ml_suggested_alt': ml_caption,
            'similarity_score': round(similarity, 3),
            'is_adequate': is_adequate,
            'recommendation': 'Current alt text is adequate' if is_adequate else 'Consider using ML-suggested alt text',
            'success': True
        }
    except Exception as e:
        return {
            'current_alt': current_alt,
            'success': False,
            'error': str(e)
        }


# Example usage
if __name__ == "__main__":
    print("=" * 70)
    print("Image Alt Text Predictor - Testing")
    print("=" * 70)
    print()
    
    # Test with a sample image URL
    test_url = "https://images.unsplash.com/photo-1518791841217-8f162f1e1131"
    
    print("Test 1: Predict alt text from URL")
    print(f"Image: {test_url[:50]}...")
    result = predict_alt_text_from_url(test_url)
    print(f"Result: {result}")
    print()
    
    print("Test 2: Suggest alt text for img tag")
    suggestion = suggest_alt_text_for_img_tag(test_url)
    print(f"Suggestion: {suggestion}")
    print()
    
    print("=" * 70)
