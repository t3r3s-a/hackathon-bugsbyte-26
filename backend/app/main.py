from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import dieta  # Rota do colega

# --- A TUA PARTE ---
# Importamos os teus ficheiros que estão na pasta /app/pag/
from app.pag import login, create, questionario 

app = FastAPI(title="Nutrium Backend")

# CORS (Mantém o que o colega fez)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- INCLUIR TODAS AS ROTAS ---

# 1. As tuas rotas de Autenticação
app.include_router(login.router, tags=["Autenticação"])
app.include_router(create.router, tags=["Autenticação"])

# 2. A tua rota de Questionário (a ponte para a IA)
app.include_router(questionario.router, prefix="/api", tags=["Inputs Nutrição"])

# 3. A rota da IA do teu colega
app.include_router(dieta.router)

@app.get("/")
def root():
    return {"status": "Backend da Nutrium a funcionar zezocas e com Login!"}