# Sentiment analysis endpoint using TextBlob
# This exposes the sentiment analyzer module through the API
from fastapi import APIRouter
from pydantic import BaseModel
from ML.sentiment_analyzer import analyze_sentiment

router = APIRouter()

class SentimentRequest(BaseModel):
    text: str
class BatchSentimentRequest(BaseModel):
    texts: list[str]

@router.post(
    "/analyze",
    summary="Analyze sentiment of text",
    description="Takes a text input and returns sentiment, confidence score, and a short summary."
)
def analyze_text(data: SentimentRequest):
    if not data.text.strip():
        return {"error": "Text input cannot be empty"}

    result = analyze_sentiment(data.text)
    return result


@router.post("/batch")
def analyze_batch(data: BatchSentimentRequest):
    """
    Analyze sentiment for multiple texts.
    """

    results = []

    for text in data.texts:
        result = analyze_sentiment(text)
        results.append(result)
    return results