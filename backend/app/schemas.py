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