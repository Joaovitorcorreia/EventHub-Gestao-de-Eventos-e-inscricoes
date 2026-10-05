from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class CadastroUsuarioSchema(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    email: EmailStr
    senha: str = Field(min_length=6, max_length=100)

class RespostaUsuarioSchema(BaseModel):
    nome: str
    email: EmailStr
    message: str

    class Config:
        from_attributes = True
    