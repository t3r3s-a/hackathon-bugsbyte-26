import re
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from app.data.alergias import alergia as LISTA_ALERGIAS_OFICIAL


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=8)

    @field_validator('password')
    @classmethod
    def validar_password(cls, v: str) -> str:
        if not re.search(r'[A-Z]', v):
            raise ValueError('A password deve ter uma letra maiúscula.')
        if not re.search(r'[!@#$%^&*()]', v):
            raise ValueError('A password deve ter um caracter especial.')
        return v

class UserLogin(BaseModel):
    username: str
    password: str

class DadosUsuario(BaseModel):
    username: str  # Precisamos disto para saber em qual user guardar
    idade: int
    peso: float
    altura: float
    sexo: str # "Masculino", "Feminino", etc.
    faz_desporto: str # "sim" ou "nao"
    frequencia_desporto: int = 0 # ex: 3 (vezes por semana)
    brinca_na_rua: str # "sim" ou "nao"
    alergias: List[str] # Lista de caixas marcadas
    quem_cozinha: str # "mae", "pai", "irmao", "avos", "outros"
    quem_cozinha_outro: Optional[str] = "" 
    come_na_cantina: str # "sim" ou "nao"
    @field_validator('alergias')
    @classmethod
    def validar_alergias_oficiais(cls, v: List[str]) -> List[str]:
        for item in v:
            if item not in LISTA_ALERGIAS_OFICIAL:
                raise ValueError(f"A alergia '{item}' não faz parte da nossa lista oficial.")
        return v


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
