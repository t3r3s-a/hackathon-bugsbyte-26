from fastapi import APIRouter, HTTPException, status
from app.schemas import UserCreate


router = APIRouter()

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def criar_conta(user: UserCreate):
    if user.username.lower() in [u.lower() for u in ...]: #adicionar base de dados
        raise HTTPException(
            status_code=400, 
            detail="Erro: Este nome de utilizador já está registado."
        )
    return {"message": f"Utilizador {user.username} criado com sucesso!"}