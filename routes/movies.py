from fastapi import APIRouter
from models import MovieRequest, RecommendationResponse, SentimentResponse
from services.recommender import recommend_movie
from services.sentiment import analyze_sentiment

router = APIRouter(prefix="/movies", tags=["Movies"])

@router.post("/recommend", response_model=RecommendationResponse)
def get_recommendation(request: MovieRequest):
    """Recomenda um filme baseado em dois escolhidos pelo usuário."""
    return recommend_movie(request.movie1, request.movie2)

@router.get("/sentiment/{movie_name}", response_model=SentimentResponse)
def get_sentiment(movie_name: str):
    """Analisa o sentimento das críticas de um filme."""
    return analyze_sentiment(movie_name)