from fastapi import FastAPI
from routes.movies import router as movies_router

app = FastAPI(title="Sistema de Recomendação Inteligente de Filmes")

# Registrar as rotas dos filmes
app.include_router(movies_router)
