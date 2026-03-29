from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime
from enum import Enum

class UserType(str, Enum):
    ALUNO = "ALUNO"
    PROFESSOR = "PROFESSOR"
    ADMIN = "ADMIN"

class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    tipo: UserType
    matricula: Optional[str] = None
    registro_professor: Optional[str] = None

class UsuarioCreate(UsuarioBase):
    senha: str

    @validator("senha")
    def validate_senha(cls, valor):
        if len(valor) < 6:
            raise ValueError("A senha deve ter no mínimo 6 caracteres")
        return valor

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    ativo: Optional[bool] = None

class UsuarioResponse(UsuarioBase):
    id: int
    ativo: bool
    data_cadastro: datetime
    ultimo_acesso: Optional[datetime]

    class Config:
        from_attributes = True

class UsuarioMessage(BaseModel):
    message: str
    usuario: UsuarioResponse

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None
    tipo: Optional[UserType] = None
