from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum
from app.schemas.presenca import PresencaResponse, EstatisticaResponse
from app.schemas.geo import Coordenadas

class ChamadaStatus(str, Enum):
    ABERTA = "ABERTA"
    ENCERRADA = "ENCERRADA"

class ChamadaBase(BaseModel):
    turma_id: int
    raio: float = Field(50.0, ge=10, le=50)

class ChamadaCreate(ChamadaBase):
    coordenadas: Coordenadas

class ChamadaUpdate(BaseModel):
    status: Optional[ChamadaStatus] = None

class ChamadaResponse(ChamadaBase):
    id: int
    professor_id: int
    coordenadas_professor: Coordenadas
    data_abertura: datetime
    data_encerramento: Optional[datetime]
    status: ChamadaStatus

    class Config:
        from_attributes = True

class ChamadaResumo(BaseModel):
    id: int
    data_abertura: datetime
    data_encerramento: Optional[datetime] = None
    raio: float
    status: str

    class Config:
        from_attributes = True

class RelatorioChamadaResponse(BaseModel):
    chamada: ChamadaResumo
    presencas: List[PresencaResponse]
    estatisticas: EstatisticaResponse
