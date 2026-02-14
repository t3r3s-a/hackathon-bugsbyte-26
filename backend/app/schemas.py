from pydantic import BaseModel
from typing import Optional

class DadosUsuario(BaseModel):
    idade: int
    peso: float
    altura: int
    objetivo: str
    restricoes: str

class MensagemChat(BaseModel):
    pergunta: str

# NOVOS SCHEMAS PARA LOGIN/REGISTO
class RegisterUser(BaseModel):
    username: str
    password: str
    email: str

class LoginUser(BaseModel):
    username: str
    password: str
