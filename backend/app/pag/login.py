# estou dependente da BD
from fastapi import APIRouter, HTTPException
from app.schemas import UserLogin

router = APIRouter()

@router.post("/login")
async def login(user: UserLogin):
    user_existe = True 
    password_correta = False 
    
    if not user_existe or not password_correta:
        
        raise HTTPException(
            status_code=401, 
            detail="Credenciais inválidas. Tenta novamente."
        )
    
    return {"message": "Bem-vindo! Login efetuado."}