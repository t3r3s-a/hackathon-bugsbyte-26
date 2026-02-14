from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import dieta
from app.routes import user_routes

app = FastAPI(title="Nutrium Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dieta.router)
app.include_router(user_routes.router, prefix="/users")

@app.get("/")
def root():
    return {"status": "Backend da Nutrium a funcionar zezocas"}
