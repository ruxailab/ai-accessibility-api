"""
Anchor Text Accessibility Classifier - Prediction Module

This module provides functions to load the trained model and predict
whether anchor text is accessible for screen readers.

Usage:
    from ML.predict import predict_anchor_text, is_anchor_text_accessible
    
    # Single prediction
    result = predict_anchor_text("click here")
    print(result)  # {'text': 'click here', 'prediction': 'bad', 'confidence': 0.95}
    
    # Boolean check
    is_good = is_anchor_text_accessible("Download the user guide")
    print(is_good)  # True
"""

import pickle
import os
from typing import Dict, List

class AnchorTextClassifier:
    """
    Wrapper class for the anchor text accessibility classifier model.
    """
    
    def __init__(self):
        self.model = None
        self.model_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'anchor_text_classifier.pkl'
        )
        self._load_model()
    
    def _load_model(self):
        """Load the trained model from disk."""
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"Model file not found at {self.model_path}. "
                f"Please run train_model.py first to train the model."
            )
        
        with open(self.model_path, 'rb') as f:
            self.model = pickle.load(f)
    
    def predict(self, text: str) -> Dict[str, any]:
        """
        Predict if anchor text is accessible for screen readers.
        
        Args:
            text: The anchor text to evaluate
            
        Returns:
            Dictionary with prediction results:
            {
                'text': str,
                'prediction': 'good' or 'bad',
                'confidence': float (0-1),
                'is_accessible': bool
            }
        """
        if not text or not isinstance(text, str):
            return {
                'text': text,
                'prediction': 'bad',
                'confidence': 0.0,
                'is_accessible': False,
                'error': 'Invalid input: text must be a non-empty string'
            }
        
        # Clean the text
        text = text.strip()
        
        if len(text) == 0:
            return {
                'text': text,
                'prediction': 'bad',
                'confidence': 1.0,
                'is_accessible': False,
                'reason': 'Empty anchor text'
            }
        
        # Make prediction
        prediction = self.model.predict([text])[0]
        probabilities = self.model.predict_proba([text])[0]
        confidence = max(probabilities)
        
        return {
            'text': text,
            'prediction': prediction,
            'confidence': round(confidence, 3),
            'is_accessible': prediction == 'good',
            'probability_good': round(probabilities[1], 3),
            'probability_bad': round(probabilities[0], 3)
        }
    
    def predict_batch(self, texts: List[str]) -> List[Dict[str, any]]:
        """
        Predict accessibility for multiple anchor texts.
        
        Args:
            texts: List of anchor text strings
            
        Returns:
            List of prediction dictionaries
        """
        return [self.predict(text) for text in texts]
    
    def is_accessible(self, text: str, confidence_threshold: float = 0.6) -> bool:
        """
        Simple boolean check if anchor text is accessible.
        
        Args:
            text: The anchor text to evaluate
            confidence_threshold: Minimum confidence required (0-1)
            
        Returns:
            True if text is predicted as 'good' with sufficient confidence
        """
        result = self.predict(text)
        return (result['is_accessible'] and 
                result['confidence'] >= confidence_threshold)


# Global instance (lazy loaded)
_classifier_instance = None

def get_classifier() -> AnchorTextClassifier:
    """Get or create the global classifier instance."""
    global _classifier_instance
    if _classifier_instance is None:
        _classifier_instance = AnchorTextClassifier()
    return _classifier_instance


# Convenience functions
def predict_anchor_text(text: str) -> Dict[str, any]:
    """
    Predict if anchor text is accessible (convenience function).
    
    Args:
        text: The anchor text to evaluate
        
    Returns:
        Dictionary with prediction results
        
    Example:
        >>> result = predict_anchor_text("click here")
        >>> print(result)
        {'text': 'click here', 'prediction': 'bad', 'confidence': 0.95, ...}
    """
    classifier = get_classifier()
    return classifier.predict(text)


def is_anchor_text_accessible(text: str, confidence_threshold: float = 0.6) -> bool:
    """
    Check if anchor text is accessible (convenience function).
    
    Args:
        text: The anchor text to evaluate
        confidence_threshold: Minimum confidence required (0-1)
        
    Returns:
        True if accessible, False otherwise
        
    Example:
        >>> is_anchor_text_accessible("Download user guide")
        True
        >>> is_anchor_text_accessible("click here")
        False
    """
    classifier = get_classifier()
    return classifier.is_accessible(text, confidence_threshold)


def predict_batch(texts: List[str]) -> List[Dict[str, any]]:
    """
    Predict accessibility for multiple anchor texts (convenience function).
    
    Args:
        texts: List of anchor text strings
        
    Returns:
        List of prediction dictionaries
        
    Example:
        >>> texts = ["click here", "Download the guide", "read more"]
        >>> results = predict_batch(texts)
        >>> for r in results:
        ...     print(f"{r['text']}: {r['prediction']}")
    """
    classifier = get_classifier()
    return classifier.predict_batch(texts)


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("Anchor Text Accessibility Classifier - Testing")
    print("=" * 60)
    print()
    
    # Test examples
    test_cases = [
        "click here",
        "read more",
        "Download the complete accessibility guide",
        "Learn more about WCAG 2.1 guidelines",
        "here",
        "Contact our support team",
        "info",
        "View our privacy policy and terms of service"
    ]
    
    print("Testing predictions:")
    print("-" * 60)
    
    for text in test_cases:
        result = predict_anchor_text(text)
        emoji = "✅" if result['is_accessible'] else "❌"
        print(f"{emoji} '{text}'")
        print(f"   Prediction: {result['prediction'].upper()}")
        print(f"   Confidence: {result['confidence']:.1%}")
        print(f"   Accessible: {result['is_accessible']}")
        print()
    
    print("=" * 60)
