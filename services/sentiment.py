import requests
import os
from transformers import pipeline
from fastapi import HTTPException

try:
    sentiment_analyzer = pipeline("sentiment-analysis")
except Exception as e:
    sentiment_analyzer = None
    print(f"Erro ao carregar o modelo de análise de sentimentos: {e}")

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"

def get_movie_reviews(movie_name, max_reviews=15, max_length=512):
    """Busca avaliações do filme no TMDb e limita o tamanho do texto."""
    if not TMDB_API_KEY:
        raise HTTPException(status_code=500, detail="A chave da API do TMDb não foi encontrada.")

    search_url = f"{TMDB_BASE_URL}/search/movie?query={movie_name}&api_key={TMDB_API_KEY}"

    try:
        search_response = requests.get(search_url)
        search_response.raise_for_status()
        search_data = search_response.json()

        if not search_data.get("results"):
            raise HTTPException(status_code=404, detail=f"Filme '{movie_name}' não encontrado no TMDb.")

        movie_id = search_data["results"][0]["id"]
        reviews_url = f"{TMDB_BASE_URL}/movie/{movie_id}/reviews?api_key={TMDB_API_KEY}"

        reviews_response = requests.get(reviews_url)
        reviews_response.raise_for_status()
        reviews_data = reviews_response.json()

        reviews = [review["content"][:max_length] for review in reviews_data.get("results", []) if "content" in review]

        return reviews[:max_reviews]

    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Erro na API do TMDb: {str(e)}")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar avaliações do filme: {str(e)}")

def analyze_sentiment(movie_name):
    """Busca avaliações do filme e analisa o sentimento."""
    if not sentiment_analyzer:
        raise HTTPException(status_code=500, detail="Falha ao carregar o modelo de análise de sentimentos.")

    reviews = get_movie_reviews(movie_name)

    if not reviews:
        return {
            "movie": movie_name,
            "sentiment": "indefinido",
            "confidence": 0.0,
            "message": "Nenhuma avaliação encontrada para este filme."
        }

    sentiments = []
    for review in reviews:
        try:
            analysis = sentiment_analyzer(review[:512])[0]
            sentiments.append(analysis)
        except Exception as e:
            print(f"Erro ao processar análise de sentimento: {e}")

    if not sentiments:
        raise HTTPException(status_code=500, detail="Falha ao processar as avaliações do filme.")

    positive_count = sum(1 for s in sentiments if s["label"] == "POSITIVE")
    negative_count = sum(1 for s in sentiments if s["label"] == "NEGATIVE")

    if positive_count > negative_count:
        sentiment = "positivo"
    elif negative_count > positive_count:
        sentiment = "negativo"
    else:
        sentiment = "neutro"

    confidence = max(positive_count, negative_count) / len(sentiments) if sentiments else 0.0

    return {
        "movie": movie_name,
        "sentiment": sentiment,
        "confidence": round(confidence, 2)
    }
