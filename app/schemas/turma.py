from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, time
from app.schemas.usuario import UsuarioResponse

class TurmaBase(BaseModel):
    codigo: str = Field(..., max_length=20)
    disciplina_id: id
    semestre: str = Field(..., max_length=6)
    ano: int
    horario: time
    data_inicio: date
    data_fim: date

class TurmaCreate(TurmaBase):
    pass

class TurmaUpdate(BaseModel):
    codigo: Optional[str] = None
    semestre: Optional[str] = None
    horario: Optional[time] = None
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None

class TurmaResponse(TurmaBase):
    id: int
    disciplina_nome: Optional[str] = None
    professores: List[UsuarioResponse] = []
    alunos: List[UsuarioResponse] = []

    class Config:
        from_attributes = True

class TurmaMessage(BaseModel):
    message: str
    turma: TurmaResponse

    class Config:
        from_attributes = True
