from pydantic import BaseModel, Field, model_validator
from typing import Optional, List, Any
from datetime import date, time
from app.schemas.usuario import UsuarioResponse

class TurmaBase(BaseModel):
    codigo: str = Field(..., max_length=20)
    disciplina_id: int
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

    @model_validator(mode="before")
    @classmethod
    def set_disciplina_nome(cls, data: Any) -> Any:
        if hasattr(data, "disciplina") and data.disciplina:
            data.disciplina_nome = data.disciplina.nome
        elif isinstance(data, dict) and data.get("disciplina"):
            data["disciplina_nome"] = data["disciplina"].nome
        return data

    class Config:
        from_attributes = True

class TurmaMessage(BaseModel):
    message: str
    turma: TurmaResponse

    class Config:
        from_attributes = True
