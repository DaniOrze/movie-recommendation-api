import requests
import os
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from dotenv import load_dotenv
from fastapi import HTTPException, status

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

        if not data.get("results"):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Filme '{movie_name}' não encontrado."
            )

        return data["results"][0]

    except requests.exceptions.HTTPError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Erro na API do TMDb: {str(e)}"
        )
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Erro na requisição: {str(e)}"
        )


def recommend_movie(movie1, movie2):
    """Recomenda um filme baseado na similaridade entre os gêneros."""
    movie1_data = get_movie_info(movie1)
    movie2_data = get_movie_info(movie2)

    movie1_genres = set(movie1_data.get("genre_ids", []))
    movie2_genres = set(movie2_data.get("genre_ids", []))

    if not movie1_genres or not movie2_genres:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Não foi possível obter os gêneros dos filmes."
        )

    all_genres = list(movie1_genres | movie2_genres)
    vec1 = np.array([1 if genre in movie1_genres else 0 for genre in all_genres])
    vec2 = np.array([1 if genre in movie2_genres else 0 for genre in all_genres])

    similarity = cosine_similarity([vec1], [vec2])[0][0]

    if similarity <= 0.1:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Os filmes não possuem similaridade suficiente para uma recomendação."
        )

    genre_query = ",".join(map(str, all_genres))
    rec_url = f"{TMDB_BASE_URL}/discover/movie?with_genres={genre_query}&api_key={TMDB_API_KEY}"

    try:
        rec_response = requests.get(rec_url)
        rec_response.raise_for_status()
        rec_data = rec_response.json()

        if not rec_data.get("results"):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhuma recomendação encontrada."
            )

        return {
            "recommended_movie": rec_data["results"][0]["title"],
            "similarity_score": similarity
        }

    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Erro ao buscar recomendações: {str(e)}"
        )
