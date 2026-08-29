# TextBlob library used for simple sentiment analysis
from textblob import TextBlob

def analyze_sentiment(text):
    """
    Analyze sentiment of input text and return standardized output.
    """

    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0:
        sentiment = "positive"
    elif polarity < 0:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return {
        "sentiment": sentiment,
        "confidence_score": abs(polarity),
        "text_summary": f"Detected {sentiment} sentiment from the given text."
    }


if __name__ == "__main__":
    sample = "I really love this product!"
    result = analyze_sentiment(sample)
    print(result)