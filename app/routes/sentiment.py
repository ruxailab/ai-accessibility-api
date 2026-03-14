# Sentiment analysis endpoint using TextBlob
# This exposes the sentiment analyzer module through the API
from fastapi import APIRouter
from pydantic import BaseModel
from ML.sentiment_analyzer import analyze_sentiment

router = APIRouter()

class SentimentRequest(BaseModel):
    text: str

@router.post("/analyze")
def analyze_text(data: SentimentRequest):
    """
    Analyze sentiment of the given text.
    """
    result = analyze_sentiment(data.text)
    return result