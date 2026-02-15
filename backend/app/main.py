import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes import dieta
from app.routes import user_routes
from app.routes import plano

app = FastAPI(title="Nutrium Backend")
app.include_router(plano.router, prefix="/plano", tags=["Plano"])
game_build_path = os.path.join(os.path.dirname(__file__), "Jogo", "build", "web")
if os.path.exists(game_build_path):
    app.mount("/play-game", StaticFiles(directory=game_build_path, html=True), name="snake")
    print("Jogo montado em http://127.0.0.1:8000/play-game")

# --- CONFIGURAÇÃO DE CAMINHOS ---
BASE_DIR = os.path.dirname(__file__)

# 1. Pasta das Imagens (Assets)
assets_path = os.path.join(BASE_DIR, "Jogo", "assets") 

# 2. Pasta do Jogo Compilado (Gerada pelo Pygbag)
# O Pygbag cria uma pasta 'build/web' dentro de 'Jogo'
game_path = os.path.join(BASE_DIR, "Jogo", "build", "web")

# --- MONTAR PASTAS ESTÁTICAS ---

# Servir imagens em http://127.0.0.1:8000/static/
if os.path.exists(assets_path):
    app.mount("/static", StaticFiles(directory=assets_path), name="static")
    print(f"✅ Imagens prontas em /static")
else:
    print(f"⚠️ Alerta: Pasta de imagens não encontrada em {assets_path}")

# Servir o Jogo em http://127.0.0.1:8000/play-game/
if os.path.exists(game_path):
    # html=True faz com que ele procure o index.html automaticamente
    app.mount("/play-game", StaticFiles(directory=game_path, html=True), name="game")
    print(f"✅ Jogo Pygame pronto em /play-game")
else:
    print(f"⚠️ Alerta: Pasta de build do jogo não encontrada. Corre o pygbag primeiro!")


# --- MIDDLEWARES E ROTAS ---

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(plano.router, prefix="/api/plano", tags=["Plano"])
app.include_router(dieta.router)
app.include_router(user_routes.router, prefix="/users")

@app.get("/")
def root():
    return {"status": "Backend da Nutrium a funcionar zezocas!"}