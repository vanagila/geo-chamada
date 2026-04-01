from sqlalchemy.orm import Session
from typing import Optional, List
from fastapi import HTTPException, status
from app.repositories.chamada_repository import ChamadaRepository
from app.schemas.chamada import ChamadaCreate, ChamadaUpdate, ChamadaResponse
from app.models.Chamada import Chamada, ChamadaStatus
from app.models.Turma import Turma
from app.utils.geo import GeoUtils

class ChamadaService:
    def __init__(self, db: Session):
        self.db = db
        self.chamada_repo = ChamadaRepository(db)

    def abrir_chamada(self, chamada_data: ChamadaCreate, professor_id: int):
        turma = self.db.query(Turma).filter(Turma.id == chamada_data.turma_id).first()
        if not turma:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Turma não encontrada"
            )

        if not any(p.id == professor_id for p in turma.professores):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Professor não pertence a turma"
            )

        if not GeoUtils.validar_coordenadas(chamada_data.coordenadas.latitude, chamada_data.coordenadas.longitude):
            raise ValueError("Coordenadas inválidas")

        chamada = self.chamada_repo.create(chamada_data, professor_id)
        return chamada

    def encerrar_chamada(self, chamada_id):
        chamada = self.chamada_repo.encerrar(chamada_id)
        if not chamada:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chamada não encontrada"
            )

        if chamada.status == ChamadaStatus.ENCERRADA:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Chamada já encerrada"
            )
        return chamada
