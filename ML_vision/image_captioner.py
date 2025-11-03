"""
Image Caption Generator using Pretrained Vision Models

This module uses pretrained models (BLIP) to generate descriptive text for images.
Useful for suggesting alt text for images in accessibility analysis.

Requirements:
    pip install transformers pillow torch requests
"""

import os
from typing import Union, Optional
from PIL import Image
import requests
from io import BytesIO
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

class ImageCaptioner:
    """
    Image captioning using BLIP (Bootstrapping Language-Image Pre-training)
    """
    
    def __init__(self, model_name: str = "Salesforce/blip-image-captioning-base"):
        """
        Initialize the image captioner with a pretrained model.
        
        Args:
            model_name: HuggingFace model identifier
                       - "Salesforce/blip-image-captioning-base" (default, ~1GB)
                       - "Salesforce/blip-image-captioning-large" (better quality, ~2GB)
        """
        print(f"🔧 Loading image captioning model: {model_name}")
        print("   This may take a moment on first run...")
        
        # Determine device (GPU if available, else CPU)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"   Using device: {self.device}")
        
        # Load processor and model
        self.processor = BlipProcessor.from_pretrained(model_name)
        self.model = BlipForConditionalGeneration.from_pretrained(model_name).to(self.device)
        
        print("✅ Model loaded successfully!")
    
    def load_image_from_url(self, url: str) -> Image.Image:
        """
        Load an image from a URL.
        
        Args:
            url: The image URL
            
        Returns:
            PIL Image object
        """
        try:
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            response.raise_for_status()
            return Image.open(BytesIO(response.content)).convert('RGB')
        except Exception as e:
            raise ValueError(f"Failed to load image from URL: {e}")
    
    def load_image_from_path(self, path: str) -> Image.Image:
        """
        Load an image from a file path.
        
        Args:
            path: Path to the image file
            
        Returns:
            PIL Image object
        """
        try:
            return Image.open(path).convert('RGB')
        except Exception as e:
            raise ValueError(f"Failed to load image from path: {e}")
    
    def generate_caption(
        self, 
        image: Union[str, Image.Image],
        max_length: int = 50,
        num_beams: int = 5
    ) -> str:
        """
        Generate a caption for an image.
        
        Args:
            image: Can be:
                   - PIL Image object
                   - File path to image
                   - URL to image
            max_length: Maximum length of generated caption
            num_beams: Number of beams for beam search (higher = better quality, slower)
            
        Returns:
            Generated caption as string
        """
        # Load image if needed
        if isinstance(image, str):
            if image.startswith(('http://', 'https://')):
                pil_image = self.load_image_from_url(image)
            else:
                pil_image = self.load_image_from_path(image)
        else:
            pil_image = image
        
        # Process image
        inputs = self.processor(pil_image, return_tensors="pt").to(self.device)
        
        # Generate caption
        with torch.no_grad():
            output = self.model.generate(
                **inputs,
                max_length=max_length,
                num_beams=num_beams,
                early_stopping=True
            )
        
        # Decode and return caption
        caption = self.processor.decode(output[0], skip_special_tokens=True)
        return caption
    
    def generate_detailed_caption(
        self,
        image: Union[str, Image.Image],
        prompt: str = "a photograph of"
    ) -> str:
        """
        Generate a more detailed caption using conditional generation.
        
        Args:
            image: Image (path, URL, or PIL Image)
            prompt: Text prompt to guide generation
            
        Returns:
            Generated detailed caption
        """
        # Load image if needed
        if isinstance(image, str):
            if image.startswith(('http://', 'https://')):
                pil_image = self.load_image_from_url(image)
            else:
                pil_image = self.load_image_from_path(image)
        else:
            pil_image = image
        
        # Process with text prompt
        inputs = self.processor(pil_image, prompt, return_tensors="pt").to(self.device)
        
        # Generate
        with torch.no_grad():
            output = self.model.generate(
                **inputs,
                max_length=75,
                num_beams=5
            )
        
        caption = self.processor.decode(output[0], skip_special_tokens=True)
        return caption


# Global instance (lazy loaded)
_captioner_instance: Optional[ImageCaptioner] = None

def get_captioner() -> ImageCaptioner:
    """Get or create the global image captioner instance."""
    global _captioner_instance
    if _captioner_instance is None:
        _captioner_instance = ImageCaptioner()
    return _captioner_instance


def generate_alt_text(image: Union[str, Image.Image], detailed: bool = False) -> str:
    """
    Generate alt text for an image (convenience function).
    
    Args:
        image: Image path, URL, or PIL Image
        detailed: If True, generate more detailed description
        
    Returns:
        Generated alt text description
        
    Example:
        >>> alt_text = generate_alt_text("https://example.com/image.jpg")
        >>> print(alt_text)
        "a dog sitting on grass"
    """
    captioner = get_captioner()
    
    if detailed:
        return captioner.generate_detailed_caption(image)
    else:
        return captioner.generate_caption(image)


def generate_alt_text_batch(images: list, detailed: bool = False) -> list:
    """
    Generate alt text for multiple images.
    
    Args:
        images: List of image paths, URLs, or PIL Images
        detailed: If True, generate more detailed descriptions
        
    Returns:
        List of generated alt text descriptions
    """
    captioner = get_captioner()
    results = []
    
    for img in images:
        try:
            if detailed:
                caption = captioner.generate_detailed_caption(img)
            else:
                caption = captioner.generate_caption(img)
            results.append({
                'image': str(img),
                'alt_text': caption,
                'success': True
            })
        except Exception as e:
            results.append({
                'image': str(img),
                'alt_text': None,
                'success': False,
                'error': str(e)
            })
    
    return results


# Example usage
if __name__ == "__main__":
    print("=" * 70)
    print("Image Caption Generator - Testing")
    print("=" * 70)
    print()
    
    # Example image URLs
    test_images = [
        "https://images.unsplash.com/photo-1518791841217-8f162f1e1131",  # Cat
        "https://images.unsplash.com/photo-1552053831-71594a27632d",  # Dog
    ]
    
    captioner = get_captioner()
    
    print("Testing with sample images:\n")
    for url in test_images[:1]:  # Test with first image
        print(f"Image: {url[:50]}...")
        try:
            caption = captioner.generate_caption(url)
            print(f"Caption: {caption}")
            print()
        except Exception as e:
            print(f"Error: {e}")
            print()
    
    print("=" * 70)
