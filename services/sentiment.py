import requests
import os
from transformers import pipeline

sentiment_analyzer = pipeline("sentiment-analysis")

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"

def get_movie_reviews(movie_name, max_reviews=5, max_length=512):
    """Busca as avaliações do filme no TMDb e limita o tamanho do texto."""
    search_url = f"{TMDB_BASE_URL}/search/movie?query={movie_name}&api_key={TMDB_API_KEY}"
    search_response = requests.get(search_url).json()

    if not search_response.get("results"):
        return []

    movie_id = search_response["results"][0]["id"]

    reviews_url = f"{TMDB_BASE_URL}/movie/{movie_id}/reviews?api_key={TMDB_API_KEY}"
    reviews_response = requests.get(reviews_url).json()

    reviews = []
    for review in reviews_response.get("results", []):
        if "content" in review:
            truncated_review = review["content"][:max_length]
            reviews.append(truncated_review)

    return reviews[:max_reviews]

def analyze_sentiment(movie_name):
    """Busca avaliações do filme e analisa o sentimento."""
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

    positive_count = sum(1 for s in sentiments if s["label"] == "POSITIVE")
    negative_count = sum(1 for s in sentiments if s["label"] == "NEGATIVE")

    if positive_count > negative_count:
        sentiment = "positivo"
    elif negative_count > positive_count:
        sentiment = "negativo"
    else:
        sentiment = "neutro"

    confidence = max(positive_count, negative_count) / max(1, len(sentiments))

    return {
        "movie": movie_name,
        "sentiment": sentiment,
        "confidence": round(confidence, 2),
        "total_reviews_analyzed": len(reviews)
    }