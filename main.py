from fastapi import FastAPI
from routes.movies import router as movies_router

app = FastAPI(
    title="Sistema de Recomendação Inteligente de Filmes",
    description="Uma API para recomendar filmes com base em similaridade de gêneros e analisar sentimentos das críticas.",
    version="1.0.0",
)

# Registrar as rotas dos filmes
app.include_router(movies_router)
