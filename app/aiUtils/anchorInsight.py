import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from collections import Counter
import spacy

# Download required NLTK data (run once)
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('stopwords')

class LinkTextAnalyzer:
    def __init__(self):
        # Load spaCy model (install with: python -m spacy download en_core_web_sm)
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("SpaCy model not found. Install with: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        # Define vague/generic link text patterns
        self.vague_patterns = [
            r'\bclick\s+here\b',
            r'\bread\s+more\b',
            r'\blearn\s+more\b',
            r'\bmore\s+info\b',
            r'\bmore\s+information\b',
            r'\bfind\s+out\s+more\b',
            r'\bsee\s+more\b',
            r'\bview\s+more\b',
            r'\bcontinue\s+reading\b',
            r'\bthis\s+link\b',
            r'\bhere\b$',
            r'^\bthis\b$',
            r'^\bthat\b$',
            r'^\bit\b$',
            r'^\blink\b$',
            r'^\burl\b$',
            r'^\bweb\s?site\b$',
            r'^\bpage\b$',
        ]
        
        # Compile patterns for efficiency
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.vague_patterns]
        
        # Common descriptive indicators
        self.descriptive_indicators = [
            'guide', 'tutorial', 'how', 'what', 'why', 'when', 'where',
            'documentation', 'manual', 'instructions', 'steps', 'process',
            'overview', 'introduction', 'basics', 'advanced', 'complete',
            'comprehensive', 'detailed', 'analysis', 'review', 'comparison'
        ]

    def extract_features(self, text):
        """Extract linguistic features from link text"""
        features = {}
        
        # Basic text features
        features['length'] = len(text.strip())
        features['word_count'] = len(text.strip().split())
        features['char_count'] = len(text.replace(' ', ''))
        
        # Check for vague patterns
        features['has_vague_pattern'] = any(pattern.search(text) for pattern in self.compiled_patterns)
        
        # Check for descriptive indicators
        text_lower = text.lower()
        features['descriptive_words'] = sum(1 for word in self.descriptive_indicators if word in text_lower)
        
        # POS tagging analysis
        try:
            tokens = word_tokenize(text)
            pos_tags = pos_tag(tokens)
            
            # Count different POS types
            pos_counts = Counter(tag for word, tag in pos_tags)
            features['noun_count'] = pos_counts.get('NN', 0) + pos_counts.get('NNS', 0) + pos_counts.get('NNP', 0) + pos_counts.get('NNPS', 0)
            features['verb_count'] = pos_counts.get('VB', 0) + pos_counts.get('VBD', 0) + pos_counts.get('VBG', 0) + pos_counts.get('VBN', 0) + pos_counts.get('VBP', 0) + pos_counts.get('VBZ', 0)
            features['adj_count'] = pos_counts.get('JJ', 0) + pos_counts.get('JJR', 0) + pos_counts.get('JJS', 0)
            
        except Exception as e:
            features['noun_count'] = 0
            features['verb_count'] = 0
            features['adj_count'] = 0
        
        # Named Entity Recognition
        if self.nlp:
            doc = self.nlp(text)
            features['entity_count'] = len(doc.ents)
            features['has_entities'] = len(doc.ents) > 0
        else:
            features['entity_count'] = 0
            features['has_entities'] = False
            
        # Specificity indicators
        features['has_numbers'] = bool(re.search(r'\d', text))
        features['has_specific_terms'] = bool(re.search(r'\b(guide|tutorial|documentation|manual|api|reference)\b', text, re.IGNORECASE))
        
        return features

    def calculate_descriptiveness_score(self, text):
        """Calculate a descriptiveness score from 0-100"""
        features = self.extract_features(text)
        score = 50  # Start with neutral score
        
        # Penalties for vague patterns
        if features['has_vague_pattern']:
            score -= 40
        
        # Rewards for length and word count
        if features['word_count'] >= 3:
            score += min(features['word_count'] * 5, 25)
        elif features['word_count'] <= 1:
            score -= 20
            
        # Rewards for descriptive content
        score += features['descriptive_words'] * 10
        score += features['noun_count'] * 5
        score += features['adj_count'] * 3
        
        # Rewards for entities and specificity
        if features['has_entities']:
            score += 15
        if features['has_numbers']:
            score += 5
        if features['has_specific_terms']:
            score += 10
            
        # Ensure score is within bounds
        return max(0, min(100, score))

    def classify_link_text(self, text):
        """Classify link text as descriptive, vague, or neutral"""
        score = self.calculate_descriptiveness_score(text)
        
        if score >= 70:
            return "Descriptive"
        elif score <= 30:
            return "Vague"
        else:
            return "Neutral"

    def analyze_link_text(self, text):
        """Complete analysis of link text"""
        features = self.extract_features(text)
        score = self.calculate_descriptiveness_score(text)
        classification = self.classify_link_text(text)
        
        # Generate suggestions for improvement
        suggestions = self.generate_suggestions(text, features, score)
        
        return {
            'text': text,
            'score': score,
            'classification': classification,
            'features': features,
            'suggestions': suggestions
        }

    def generate_suggestions(self, text, features, score):
        """Generate improvement suggestions"""
        suggestions = []
        
        if features['has_vague_pattern']:
            suggestions.append("Remove vague phrases like 'click here' or 'read more'")
            
        if features['word_count'] < 3:
            suggestions.append("Add more descriptive words to explain the destination")
            
        if features['noun_count'] == 0:
            suggestions.append("Include specific nouns that describe the content")
            
        if not features['has_entities'] and not features['has_specific_terms']:
            suggestions.append("Add specific terms or proper nouns to increase clarity")
            
        if score < 50:
            suggestions.append("Consider describing what the user will find or accomplish")
            
        return suggestions

    def batch_analyze(self, link_texts):
        """Analyze multiple link texts"""
        results = []
        for text in link_texts:
            results.append(self.analyze_link_text(text))
        return results

# Example usage
def main():
    analyzer = LinkTextAnalyzer()
    
    # Test examples
    test_links = [
        "click here",
        "read more",
        "Complete Python Tutorial for Beginners",
        "API Documentation",
        "Download the 2024 Annual Report",
        "here",
        "User Authentication Guide",
        "this link",
        "How to Install Docker on Ubuntu 22.04",
        "more info"
    ]
    
    print("Link Text Descriptiveness Analysis")
    print("=" * 50)
    
    for link_text in test_links:
        result = analyzer.analyze_link_text(link_text)
        
        print(f"\nText: '{result['text']}'")
        print(f"Score: {result['score']}/100")
        print(f"Classification: {result['classification']}")
        
        if result['suggestions']:
            print("Suggestions for improvement:")
            for suggestion in result['suggestions']:
                print(f"  • {suggestion}")
        else:
            print("✓ This link text is descriptive!")

if __name__ == "__main__":
    main()