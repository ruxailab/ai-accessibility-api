"""
Anchor Text Accessibility Classifier - Training Script

This script trains a machine learning model to classify anchor text as 'good' or 'bad'
for screen reader accessibility. The model uses TF-IDF vectorization and Logistic Regression.

Usage:
    python train_model.py
    
Output:
    - anchor_text_classifier.pkl: Trained model pipeline
    - Training accuracy and sample predictions
"""

import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import os

def train_anchor_text_classifier():
    """
    Train a text classification model to identify good vs bad anchor text
    for screen reader accessibility.
    """
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, 'training_data.csv')
    model_path = os.path.join(script_dir, 'anchor_text_classifier.pkl')
    
    print("=" * 60)
    print("Anchor Text Accessibility Classifier - Training")
    print("=" * 60)
    print()
    
    # Load the training data
    print(f"📂 Loading training data from: {data_path}")
    df = pd.read_csv(data_path)
    
    print(f"✓ Loaded {len(df)} examples")
    print(f"  - Good examples: {len(df[df['label'] == 'good'])}")
    print(f"  - Bad examples: {len(df[df['label'] == 'bad'])}")
    print()
    
    # Prepare features and labels
    X = df['text']
    y = df['label']
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"📊 Data split:")
    print(f"  - Training set: {len(X_train)} examples")
    print(f"  - Test set: {len(X_test)} examples")
    print()
    
    # Create a pipeline with TF-IDF vectorizer and Logistic Regression
    print("🔧 Building model pipeline...")
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(
            max_features=1000,  # Increased vocabulary size
            ngram_range=(1, 2),  # Use unigrams and bigrams
            lowercase=True,
            min_df=1,  # Minimum document frequency
            max_df=0.9  # Maximum document frequency
        )),
        ('classifier', LogisticRegression(
            max_iter=2000,
            random_state=42,
            C=0.5,  # Increased regularization
            class_weight='balanced'  # Handle class imbalance
        ))
    ])
    
    # Train the model
    print("🚀 Training the model...")
    pipeline.fit(X_train, y_train)
    print("✓ Training complete!")
    print()
    
    # Evaluate on test set
    print("📈 Evaluating model performance...")
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"Accuracy: {accuracy:.2%}")
    print()
    print("Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['bad', 'good']))
    
    print("Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred, labels=['bad', 'good'])
    print(f"                Predicted")
    print(f"              bad    good")
    print(f"Actual  bad   {cm[0][0]:3d}    {cm[0][1]:3d}")
    print(f"        good  {cm[1][0]:3d}    {cm[1][1]:3d}")
    print()
    
    # Save the trained model
    print(f"💾 Saving model to: {model_path}")
    with open(model_path, 'wb') as f:
        pickle.dump(pipeline, f)
    print("✓ Model saved successfully!")
    print()
    
    # Test with some example predictions
    print("🧪 Testing with sample predictions:")
    print("-" * 60)
    
    test_examples = [
        "click here",
        "Download the accessibility compliance guide",
        "read more",
        "View our privacy policy and terms of service",
        "here",
        "Contact our support team for assistance",
        "more info",
        "Learn about WCAG 2.1 guidelines"
    ]
    
    for text in test_examples:
        prediction = pipeline.predict([text])[0]
        probability = pipeline.predict_proba([text])[0]
        confidence = max(probability) * 100
        
        emoji = "✅" if prediction == "good" else "❌"
        pred_str = str(prediction).upper()
        print(f"{emoji} '{text}'")
        print(f"   Prediction: {pred_str} (confidence: {confidence:.1f}%)")
        print()
    
    print("=" * 60)
    print("Training Complete! ✨")
    print("=" * 60)
    
    return pipeline

if __name__ == "__main__":
    train_anchor_text_classifier()
