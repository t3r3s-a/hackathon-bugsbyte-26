from fastapi import APIRouter, HTTPException
from app.schemas import RegisterUser, LoginUser
from app.services.user_service import create_user, authenticate_user

router = APIRouter()

@router.post("/register")
def register(user: RegisterUser):
    success = create_user(user.dict())
    if not success:
        raise HTTPException(status_code=400, detail="Username ou email já existe")
    return {"message": "Conta criada com sucesso!"}

@router.post("/login")
def login(user: LoginUser):
    valid = authenticate_user(user.username, user.password)
    if not valid:
        raise HTTPException(status_code=400, detail="Username ou password inválido")
    return {"message": f"Bem-vindo, {user.username}!"}
