from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum
from app.schemas.chamada import Coordenadas

class PresencaStatus(str, Enum):
    PRESENTE = "PRESENTE"
    AUSENTE = "AUSENTE"
    ABONADA = "ABONADA"

class PresencaBase(BaseModel):
    chamada_id: int

class PresencaCreate(PresencaBase):
    coordenadas: Coordenadas
 
class PresencaUpdate(BaseModel):
    status: Optional[PresencaStatus] = None

class PresencaResponse(BaseModel):
    id: int
    aluno_id: int
    chamada_id: int
    distancia_calculada: Optional[float]
    data_registro: datetime
    status: PresencaStatus
    dentro_raio: bool

    class Config:
        from_attributes = True

class AbonoRequest(BaseModel):
    presenca_id: int
    motivo: str

class DisciplinaResumo(BaseModel):
    id: int
    nome: str
    codigo: str

class EstatisticaResponse(BaseModel):
    total: int
    presentes: int
    ausentes: int
    abonadas: int

class HistoricoAlunoDisciplinaResponse(BaseModel):
    disciplina: DisciplinaResumo
    presencas: List[PresencaResponse]
    estatisticas: EstatisticaResponse
