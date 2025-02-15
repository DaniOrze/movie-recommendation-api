from pydantic import BaseModel

class MovieRequest(BaseModel):
    movie1: str
    movie2: str

class RecommendationResponse(BaseModel):
    recommended_movie: str
    similarity_score: float

class SentimentResponse(BaseModel):
    movie: str
    sentiment: str
    confidence: float
