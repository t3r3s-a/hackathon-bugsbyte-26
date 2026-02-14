import re
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

# --- 1. TEUS SCHEMAS (Autenticação que tu criaste) ---
# O teu colega não tem isto, por isso tens de manter!

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

# --- 2. SCHEMAS DO TEU COLEGA (Copiados exatamente do .py dele) ---

class DadosUsuario(BaseModel):
    idade: int
    peso: float
    altura: int
    objetivo: str
    restricoes: str # O que ele vai receber da tua "ponte"

class MensagemChat(BaseModel):
    pergunta: str

# --- 3. TEU SCHEMA DE INPUT (Para as Checkboxes do site) ---

class QuestionarioInput(BaseModel):
    idade: int
    peso: float
    altura: int
    objetivo: str
    alergias: List[str] # Tu recebes a lista do frontend
    outros: Optional[str] = None