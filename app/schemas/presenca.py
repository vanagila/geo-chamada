from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum
from app.schemas.geo import Coordenadas

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

class AbonoDetailResponse(BaseModel):
    id: int
    aluno_id: int
    chamada_id: int
    status: str
    distancia_calculada: Optional[float]
    data_registro: datetime
    abonado_por_id: int
    data_abono: datetime
    motivo_abono: str

class AbonoResponse(BaseModel):
    message: str
    presenca: AbonoDetailResponse

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
