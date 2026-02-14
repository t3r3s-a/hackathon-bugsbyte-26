import json
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()
DB_FILE = "database.json"

# --- 1. MODELOS DE DADOS ---

class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserQuestionnaire(BaseModel):
    username: str
    peso: float
    altura: int
    objetivo: str
    restricoes: str
    exercicio_fisico: str
    frequencia_exercicio: str

# --- 2. FUNÇÕES AUXILIARES ---

def load_db():
    if not os.path.exists(DB_FILE):
        return {"users": []}
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return {"users": []}

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- 3. ROTAS ATUALIZADAS ---

@router.post("/register")
def register(user: UserRegister):
    db = load_db()
    if any(u["username"] == user.username for u in db["users"]):
        raise HTTPException(status_code=400, detail="Utilizador já existe")

    new_user = {
        "username": user.username,
        "email": user.email,
        "password": user.password,
        "questionnaire": None 
    }
    db["users"].append(new_user)
    save_db(db)
    return {"status": "success", "message": "Conta criada!"}

@router.post("/login")
def login(user: UserLogin):
    db = load_db()
    for u in db["users"]:
        if u["username"] == user.username and u["password"] == user.password:
            return {
                "status": "success",
                "username": u["username"],
                "email": u["email"],
                "questionnaire": u["questionnaire"]
            }
    raise HTTPException(status_code=401, detail="Dados incorretos")

# NOVA ROTA: Obter perfil (Útil para o Amigo Presente/IA saber com quem fala)
@router.get("/profile/{username}")
def get_profile(username: str):
    db = load_db()
    for u in db["users"]:
        if u["username"] == username:
            return u
    raise HTTPException(status_code=404, detail="Utilizador não encontrado")

@router.post("/save-profile")
def save_profile(data: UserQuestionnaire):
    db = load_db()
    for u in db["users"]:
        if u["username"] == data.username:
            # Atualiza apenas o campo questionnaire
            u["questionnaire"] = data.dict()
            save_db(db)
            return {"status": "success", "message": "Questionário guardado!"}
    raise HTTPException(status_code=404, detail="Utilizador não encontrado")