from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class Coordenadas(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

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
    coordenadas_professor: dict
    data_abertura: datetime
    data_encerramento: Optional[datetime]
    status: ChamadaStatus

    class Config:
        from_attributes = True

