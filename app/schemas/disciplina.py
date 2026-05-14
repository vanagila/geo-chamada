from pydantic import BaseModel, Field
from typing import Optional, List

class DisciplinaBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100)
    codigo: str = Field(..., max_length=20)
    descricao: Optional[str] = Field(None, max_length=500)
    carga_horaria: int = Field(60, ge=30, le=60, description="Carga horária em horas")

class DisciplinaCreate(DisciplinaBase):
    pass

class DisciplinaUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    carga_horaria: Optional[int] = Field(None, ge=30, le=240)

class DisciplinaResponse(DisciplinaBase):
    id: int
    turmas_count: Optional[int] = 0

    class Config:
        from_attributes = True

class DisciplinaMessage(BaseModel):
    message: str
    disciplina: DisciplinaResponse

    class Config:
        from_attributes = True
