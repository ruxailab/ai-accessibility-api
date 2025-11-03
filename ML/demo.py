"""
Demo: How to use the Anchor Text Accessibility Classifier

This script demonstrates various ways to use the ML model
to check if anchor text is accessible for screen readers.
"""

from predict import predict_anchor_text, is_anchor_text_accessible, predict_batch

def demo_single_prediction():
    """Demo: Single text prediction with detailed results"""
    print("=" * 70)
    print("DEMO 1: Single Prediction with Detailed Results")
    print("=" * 70)
    print()
    
    texts_to_test = [
        "click here",
        "Download the user manual",
        "read more",
        "Learn about accessibility best practices",
        "here",
    ]
    
    for text in texts_to_test:
        result = predict_anchor_text(text)
        print(f"Text: '{text}'")
        print(f"├─ Prediction: {result['prediction'].upper()}")
        print(f"├─ Accessible: {result['is_accessible']}")
        print(f"├─ Confidence: {result['confidence']:.1%}")
        print(f"├─ Probability (Good): {result['probability_good']:.1%}")
        print(f"└─ Probability (Bad): {result['probability_bad']:.1%}")
        print()
    print()


def demo_simple_boolean_check():
    """Demo: Simple boolean accessibility check"""
    print("=" * 70)
    print("DEMO 2: Simple Boolean Accessibility Check")
    print("=" * 70)
    print()
    
    link_texts = [
        "click here",
        "Download the accessibility guide PDF",
        "more info",
        "Contact our support team for help",
        "View our privacy policy",
        "learn more",
    ]
    
    print("Checking which anchor texts are accessible:\n")
    for text in link_texts:
        is_accessible = is_anchor_text_accessible(text)
        status = "✅ GOOD" if is_accessible else "❌ BAD"
        print(f"{status} - '{text}'")
    print()


def demo_batch_prediction():
    """Demo: Batch predictions for multiple texts"""
    print("=" * 70)
    print("DEMO 3: Batch Prediction")
    print("=" * 70)
    print()
    
    anchor_texts = [
        "click here",
        "here",
        "Download complete documentation",
        "Learn about WCAG 2.1 compliance",
        "read more",
        "Submit your feedback",
    ]
    
    print(f"Analyzing {len(anchor_texts)} anchor texts...\n")
    results = predict_batch(anchor_texts)
    
    # Group by prediction
    good_texts = [r for r in results if r['is_accessible']]
    bad_texts = [r for r in results if not r['is_accessible']]
    
    print(f"✅ ACCESSIBLE ({len(good_texts)}):")
    for r in good_texts:
        print(f"   • '{r['text']}' (confidence: {r['confidence']:.1%})")
    print()
    
    print(f"❌ NOT ACCESSIBLE ({len(bad_texts)}):")
    for r in bad_texts:
        print(f"   • '{r['text']}' (confidence: {r['confidence']:.1%})")
    print()


def demo_integration_example():
    """Demo: How to integrate with linksense analysis"""
    print("=" * 70)
    print("DEMO 4: Integration Example (Simulated)")
    print("=" * 70)
    print()
    
    # Simulated anchor tags from a webpage
    simulated_anchors = [
        {"text": "click here", "href": "/about"},
        {"text": "Read our privacy policy", "href": "/privacy"},
        {"text": "more", "href": "/blog"},
        {"text": "Contact support team", "href": "/contact"},
        {"text": "Download Q3 report", "href": "/reports/q3.pdf"},
    ]
    
    print("Analyzing anchor tags from a webpage:\n")
    
    issues = []
    for anchor in simulated_anchors:
        result = predict_anchor_text(anchor['text'])
        
        if not result['is_accessible']:
            issues.append({
                'text': anchor['text'],
                'href': anchor['href'],
                'confidence': result['confidence'],
                'issue': 'Non-accessible anchor text detected by ML model'
            })
    
    if issues:
        print(f"⚠️  Found {len(issues)} accessibility issues:\n")
        for i, issue in enumerate(issues, 1):
            print(f"{i}. Anchor: '{issue['text']}'")
            print(f"   Link: {issue['href']}")
            print(f"   Issue: {issue['issue']}")
            print(f"   Confidence: {issue['confidence']:.1%}")
            print()
    else:
        print("✅ No accessibility issues found!")
    print()


def demo_confidence_threshold():
    """Demo: Using confidence thresholds"""
    print("=" * 70)
    print("DEMO 5: Confidence Threshold Tuning")
    print("=" * 70)
    print()
    
    text = "Learn more about our services"
    result = predict_anchor_text(text)
    
    print(f"Testing: '{text}'")
    print(f"Prediction: {result['prediction']}")
    print(f"Confidence: {result['confidence']:.1%}\n")
    
    thresholds = [0.5, 0.6, 0.7, 0.8]
    
    print("Results with different confidence thresholds:\n")
    for threshold in thresholds:
        is_acceptable = is_anchor_text_accessible(text, confidence_threshold=threshold)
        status = "✅ Pass" if is_acceptable else "❌ Fail"
        print(f"  Threshold {threshold:.0%}: {status}")
    print()


if __name__ == "__main__":
    print("\n")
    print("🤖 ANCHOR TEXT ACCESSIBILITY CLASSIFIER - DEMO")
    print()
    
    # Run all demos
    demo_single_prediction()
    demo_simple_boolean_check()
    demo_batch_prediction()
    demo_integration_example()
    demo_confidence_threshold()
    
    print("=" * 70)
    print("Demo Complete! ✨")
    print("=" * 70)
    print()
    print("Next Steps:")
    print("  1. Integrate into your linksense analyzer")
    print("  2. Adjust confidence thresholds as needed")
    print("  3. Add more training data to improve accuracy")
    print()
