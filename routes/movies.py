from fastapi import APIRouter
from models import MovieRequest, RecommendationResponse, SentimentResponse
from services.recommender import recommend_movie
from services.sentiment import analyze_sentiment

router = APIRouter(prefix="/movies", tags=["Movies"])

@router.post("/recommend", response_model=RecommendationResponse, summary="Recomendar um filme", description="Recomenda um filme baseado na similaridade de gêneros entre dois filmes fornecidos pelo usuário.")
def get_recommendation(request: MovieRequest):
    """
    Recomendação de Filme
    
    - **movie1**: Nome do primeiro filme.
    - **movie2**: Nome do segundo filme.
    
    Retorna um filme recomendado baseado nos gêneros compartilhados.
    """
    return recommend_movie(request.movie1, request.movie2)

@router.get("/sentiment/{movie_name}", response_model=SentimentResponse, summary="Analisar sentimento", description="Analisa o sentimento das críticas de um filme específico.")
def get_sentiment(movie_name: str):
    """
    Análise de Sentimento
    
    - **movie_name**: Nome do filme a ser analisado.
    
    Retorna se o sentimento das críticas do filme é positivo, negativo ou neutro.
    """
    return analyze_sentiment(movie_name)
