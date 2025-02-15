import requests
import os
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"

def get_movie_info(movie_name):
    """Busca o ID e os detalhes do filme na API do TMDb."""
    url = f"{TMDB_BASE_URL}/search/movie?query={movie_name}&api_key={TMDB_API_KEY}"
    
    response = requests.get(url).json()
    results = response.get("results", [])
    
    if not results:
        return None
    return results[0]

def recommend_movie(movie1, movie2):
    """Recomenda um filme baseado na similaridade entre os gêneros e palavras-chave."""
    movie1_data = get_movie_info(movie1)
    movie2_data = get_movie_info(movie2)

    if not movie1_data or not movie2_data:
        return {"error": "Um dos filmes não foi encontrado."}

    movie1_genres = set(movie1_data.get("genre_ids", []))
    movie2_genres = set(movie2_data.get("genre_ids", []))
    
    all_genres = list(movie1_genres | movie2_genres)
    vec1 = np.array([1 if genre in movie1_genres else 0 for genre in all_genres])
    vec2 = np.array([1 if genre in movie2_genres else 0 for genre in all_genres])

    similarity = cosine_similarity([vec1], [vec2])[0][0]
    
    recommended_movie = None
    
    if similarity <= 0.1:
        return {
            "message": "Os filmes não possuem similaridade suficiente para uma recomendação.",
            "similarity_score": similarity
        }

    genre_query = ",".join(map(str, all_genres))
    rec_url = f"{TMDB_BASE_URL}/discover/movie?with_genres={genre_query}&api_key={TMDB_API_KEY}"
    rec_response = requests.get(rec_url).json()
    recommended_movie = rec_response["results"][0]["title"] if rec_response["results"] else "Nenhuma recomendação encontrada"

    return {
        "recommended_movie": recommended_movie,
        "similarity_score": similarity
    }
