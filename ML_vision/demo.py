"""
Demo: Image Alt Text Generation using Pretrained Vision Models

This script demonstrates how to use the ML_vision module to generate
alt text suggestions for images.

Note: This will download the BLIP model (~990MB) on first run.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from predict import (
    predict_alt_text_from_url,
    predict_alt_text_from_file,
    suggest_alt_text_for_img_tag,
    batch_predict_alt_text,
    is_alt_text_adequate
)


def demo_url_prediction():
    """Demo: Generate alt text from image URL"""
    print("=" * 70)
    print("DEMO 1: Generate Alt Text from Image URL")
    print("=" * 70)
    print()
    
    # Sample images from Unsplash (free to use)
    test_images = [
        {
            'url': 'https://images.unsplash.com/photo-1518791841217-8f162f1e1131',
            'description': 'Cat image'
        },
        {
            'url': 'https://images.unsplash.com/photo-1552053831-71594a27632d',
            'description': 'Dog image'
        }
    ]
    
    for img in test_images[:1]:  # Test with first image only for demo
        print(f"Testing: {img['description']}")
        print(f"URL: {img['url'][:60]}...")
        print()
        
        result = predict_alt_text_from_url(img['url'])
        
        if result['success']:
            print(f"✅ Generated Alt Text: \"{result['alt_text']}\"")
            print(f"   Method: {result['method']}")
        else:
            print(f"❌ Failed: {result.get('error')}")
        print()
    
    print()


def demo_img_tag_suggestion():
    """Demo: Suggest alt text for img tags"""
    print("=" * 70)
    print("DEMO 2: Suggest Alt Text for <img> Tags")
    print("=" * 70)
    print()
    
    # Simulate img tag src attributes from a webpage
    img_srcs = [
        "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba",  # Cat
        "https://images.unsplash.com/photo-1517849845537-4d257902454a",  # Dog
    ]
    
    for i, src in enumerate(img_srcs[:1], 1):
        print(f"Image {i}: {src[:60]}...")
        
        suggestion = suggest_alt_text_for_img_tag(src)
        
        if suggestion['success']:
            print(f"   HTML: <img src=\"...\" alt=\"{suggestion['suggested_alt']}\">")
            print(f"   ✅ Suggested Alt: \"{suggestion['suggested_alt']}\"")
        else:
            print(f"   ❌ Error: {suggestion.get('error')}")
        print()
    
    print()


def demo_batch_processing():
    """Demo: Process multiple images at once"""
    print("=" * 70)
    print("DEMO 3: Batch Processing Multiple Images")
    print("=" * 70)
    print()
    
    # List of images from a hypothetical webpage
    image_sources = [
        "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085",  # Coffee
        "https://images.unsplash.com/photo-1484788984921-03950022c9ef",  # Laptop
        "https://images.unsplash.com/photo-1542291026-7eec264c27ff",  # Shoes
    ]
    
    print(f"Processing {len(image_sources)} images...\n")
    
    results = batch_predict_alt_text(image_sources[:2])  # Process first 2 for demo
    
    for i, result in enumerate(results, 1):
        print(f"Image {i}:")
        print(f"  Source: {result['src'][:60]}...")
        if result['success']:
            print(f"  ✅ Alt Text: \"{result['suggested_alt']}\"")
        else:
            print(f"  ❌ Error: {result.get('error')}")
        print()
    
    print()


def demo_alt_text_evaluation():
    """Demo: Evaluate existing alt text"""
    print("=" * 70)
    print("DEMO 4: Evaluate Existing Alt Text Quality")
    print("=" * 70)
    print()
    
    # Test cases with existing alt text
    test_cases = [
        {
            'src': 'https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba',
            'current_alt': 'image',  # Bad alt text
        },
        {
            'src': 'https://images.unsplash.com/photo-1517849845537-4d257902454a',
            'current_alt': 'a brown and white dog sitting on grass',  # Good alt text
        }
    ]
    
    for i, case in enumerate(test_cases[:1], 1):
        print(f"Test Case {i}:")
        print(f"  Current Alt: \"{case['current_alt']}\"")
        print(f"  Image: {case['src'][:60]}...")
        print()
        
        assessment = is_alt_text_adequate(case['current_alt'], case['src'])
        
        if assessment['success']:
            print(f"  ML Suggestion: \"{assessment['ml_suggested_alt']}\"")
            print(f"  Similarity Score: {assessment['similarity_score']:.1%}")
            print(f"  Is Adequate: {'✅ Yes' if assessment['is_adequate'] else '❌ No'}")
            print(f"  Recommendation: {assessment['recommendation']}")
        else:
            print(f"  ❌ Error: {assessment.get('error')}")
        print()
    
    print()


def demo_integration_example():
    """Demo: How to integrate with AltSense"""
    print("=" * 70)
    print("DEMO 5: Integration with AltSense (Simulated)")
    print("=" * 70)
    print()
    
    # Simulate img tags from a webpage
    simulated_img_tags = [
        {'src': 'https://example.com/product1.jpg', 'alt': ''},
        {'src': 'https://example.com/product2.jpg', 'alt': 'image'},
        {'src': 'https://example.com/logo.jpg', 'alt': 'Company logo'},
    ]
    
    print("Analyzing images from webpage...\n")
    
    issues = []
    for img in simulated_img_tags[:1]:  # Analyze first image for demo
        current_alt = img.get('alt', '')
        src = img.get('src', '')
        
        print(f"Image: {src}")
        print(f"Current Alt: \"{current_alt}\"")
        
        # Check if alt is missing or vague
        if not current_alt or current_alt.lower() in ['image', 'photo', 'picture']:
            # Don't actually call API in demo, just show what would happen
            print("  ⚠️  Issue: Missing or vague alt text")
            print("  💡 Would generate ML suggestion here")
            print()
            
            issues.append({
                'src': src,
                'issue': 'Missing or vague alt text',
                'current_alt': current_alt,
                'ml_suggestion_available': True
            })
    
    if issues:
        print(f"\n⚠️  Found {len(issues)} accessibility issues")
        print("   ML suggestions would be provided for each")
    else:
        print("✅ No accessibility issues found!")
    
    print()


def demo_standard_vs_detailed():
    """Demo: Compare standard vs detailed captions"""
    print("=" * 70)
    print("DEMO 6: Standard vs Detailed Descriptions")
    print("=" * 70)
    print()
    
    test_url = "https://images.unsplash.com/photo-1518791841217-8f162f1e1131"
    
    print(f"Image: {test_url[:60]}...\n")
    
    # Standard caption
    print("Standard caption:")
    result_standard = predict_alt_text_from_url(test_url, detailed=False)
    if result_standard['success']:
        print(f"  \"{result_standard['alt_text']}\"")
    print()
    
    # Detailed caption
    print("Detailed caption:")
    result_detailed = predict_alt_text_from_url(test_url, detailed=True)
    if result_detailed['success']:
        print(f"  \"{result_detailed['alt_text']}\"")
    print()
    
    print()


if __name__ == "__main__":
    print("\n")
    print("🤖 IMAGE ALT TEXT GENERATOR - DEMO")
    print("📸 Using BLIP Pretrained Vision Model")
    print()
    print("⚠️  Note: This will download the model (~990MB) on first run")
    print("   Subsequent runs will use cached model")
    print()
    
    try:
        # Run demos
        # Note: Commented out actual ML demos to avoid long execution
        # Uncomment to test with actual model
        
        print("=" * 70)
        print("DEMO MODE: Showing structure without model execution")
        print("=" * 70)
        print()
        print("To run with actual model:")
        print("  1. Ensure dependencies are installed:")
        print("     pip install transformers torch pillow requests")
        print("  2. Uncomment the demo function calls in demo.py")
        print("  3. Run: python demo.py")
        print()
        print("Available demos:")
        print("  - demo_url_prediction()")
        print("  - demo_img_tag_suggestion()")
        print("  - demo_batch_processing()")
        print("  - demo_alt_text_evaluation()")
        print("  - demo_integration_example()")
        print("  - demo_standard_vs_detailed()")
        print()
        
        # Uncomment these to run actual demos:
        # demo_url_prediction()
        # demo_img_tag_suggestion()
        # demo_batch_processing()
        # demo_alt_text_evaluation()
        demo_integration_example()
        # demo_standard_vs_detailed()
        
        print("=" * 70)
        print("Demo Complete! ✨")
        print("=" * 70)
        print()
        print("Next Steps:")
        print("  1. Install required dependencies")
        print("  2. Test with your own images")
        print("  3. Integrate into AltSense analyzer")
        print("  4. Adjust confidence thresholds as needed")
        print()
        
    except Exception as e:
        print(f"\n❌ Error running demos: {e}")
        print("\nMake sure you have installed the required dependencies:")
        print("  pip install transformers torch pillow requests")
        print()
