from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
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

    @field_validator("senha")
    @classmethod
    def validate_senha(cls, valor: str):
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

    model_config = ConfigDict(from_attributes = True)

class UsuarioMessage(BaseModel):
    message: str
    usuario: UsuarioResponse

    model_config = ConfigDict(from_attributes = True)
