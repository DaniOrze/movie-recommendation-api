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
    
    try:
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()
        
        if "status_code" in data and data["status_code"] != 200:
            return {"error": f"Erro na API do TMDb: {data.get('status_message', 'Erro desconhecido')}"}
        
        results = data.get("results", [])
        if not results:
            return {"error": f"Filme '{movie_name}' não encontrado."}
        
        return results[0]
    
    except requests.exceptions.RequestException as e:
        return {"error": f"Erro na requisição à API do TMDb: {str(e)}"}

def recommend_movie(movie1, movie2):
    """Recomenda um filme baseado na similaridade entre os gêneros e palavras-chave."""
    
    movie1_data = get_movie_info(movie1)
    movie2_data = get_movie_info(movie2)

    if "error" in movie1_data or "error" in movie2_data:
        return {"error": movie1_data.get("error", movie2_data.get("error"))}

    movie1_genres = set(movie1_data.get("genre_ids", []))
    movie2_genres = set(movie2_data.get("genre_ids", []))

    if not movie1_genres or not movie2_genres:
        return {"error": "Não foi possível obter os gêneros dos filmes."}

    all_genres = list(movie1_genres | movie2_genres)
    vec1 = np.array([1 if genre in movie1_genres else 0 for genre in all_genres])
    vec2 = np.array([1 if genre in movie2_genres else 0 for genre in all_genres])

    similarity = cosine_similarity([vec1], [vec2])[0][0]

    if similarity <= 0.1:
        return {
            "message": "Os filmes não possuem similaridade suficiente para uma recomendação.",
            "similarity_score": similarity
        }

    genre_query = ",".join(map(str, all_genres))
    rec_url = f"{TMDB_BASE_URL}/discover/movie?with_genres={genre_query}&api_key={TMDB_API_KEY}"

    try:
        rec_response = requests.get(rec_url)
        rec_response.raise_for_status()
        rec_data = rec_response.json()

        if "status_code" in rec_data and rec_data["status_code"] != 200:
            return {"error": f"Erro na API do TMDb: {rec_data.get('status_message', 'Erro desconhecido')}"}

        recommended_movie = rec_data["results"][0]["title"] if rec_data["results"] else "Nenhuma recomendação encontrada"

        return {
            "recommended_movie": recommended_movie,
            "similarity_score": similarity
        }

    except requests.exceptions.RequestException as e:
        return {"error": f"Erro ao buscar recomendações: {str(e)}"}