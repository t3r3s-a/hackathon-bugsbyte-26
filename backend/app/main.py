from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import dieta

app = FastAPI(title="Nutrium Backend")

# CORS: Vital para o teu amigo do Frontend não ter erros de bloqueio
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir as rotas que acabaste de criar
app.include_router(dieta.router)

@app.get("/")
def root():
    return {"status": "Backend da Nutrium a funcionar zezocas"}