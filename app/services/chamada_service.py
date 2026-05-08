from sqlalchemy.orm import Session
from typing import Optional, List
from fastapi import HTTPException, status
from app.repositories.chamada_repository import ChamadaRepository
from app.schemas.chamada import ChamadaCreate, ChamadaUpdate, ChamadaResponse
from app.models.Chamada import Chamada, ChamadaStatus
from app.repositories.presenca_repository import PresencaRepository
from app.models.Turma import Turma
from app.utils.geo import GeoUtils
from app.utils.presenca_mapper import presenca_to_response
from app.utils.chamada_mapper import chamada_to_response
from geoalchemy2.shape import to_shape

class ChamadaService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = ChamadaRepository(db)
        self.presenca_repo = PresencaRepository(db) 

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

        chamada = self.repository.create(chamada_data, professor_id)

        ponto_geom = to_shape(chamada.coordenadas_professor)
        chamada.coordenadas_professor = {
            "latitude": ponto_geom.y,
            "longitude": ponto_geom.x
        }
        return chamada

    def encerrar(self, chamada_id: int) -> ChamadaResponse:
        chamada = self.repository.get_by_id(chamada_id)
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
        chamada_atualizada = self.repository.encerrar(chamada)
        return chamada_to_response(chamada_atualizada)

    def get_by_id(self, chamada_id: int) -> ChamadaResponse:
        chamada = self.repository.get_by_id(chamada_id)
        if not chamada:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chamada não encontrada"
            )
        return chamada_to_response(chamada)

    def get_by_turma(self, turma_id: int, skip: int = 0, limit: int = 100) -> List[ChamadaResponse]:
        chamadas = self.repository.get_by_turma(turma_id, skip=skip, limit=limit)
        return [chamada_to_response(c) for c in chamadas]

    def get_by_professor(self, professor_id: int, skip: int = 0, limit: int = 100) -> List[ChamadaResponse]:
        chamadas = self.repository.get_by_professor(professor_id, skip=skip, limit=limit)
        return [chamada_to_response(c) for c in chamadas]

    def relatorio_chamada(self, chamada_id: int) -> dict:
        chamada = self.repository.get_by_id(chamada_id)
        if not chamada:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chamada não encontrada"
            )
        presencas = self.presenca_repo.get_by_chamada(chamada_id)
        presencas_serializaveis = [presenca_to_response(p) for p in presencas]
        return {
            "chamada": {
                "id": chamada.id,
                "data_abertura": chamada.data_abertura,
                "data_encerramento": chamada.data_encerramento,
                "raio": chamada.raio,
                "status": chamada.status
            },
            "presencas": presencas_serializaveis,
            "estatisticas": {
                "total": len(presencas),
                "presentes": sum(1 for p in presencas if p.status.value == "PRESENTE"),
                "ausentes": sum(1 for p in presencas if p.status.value == "AUSENTE"),
                "abonadas": sum(1 for p in presencas if p.status.value == "ABONADA")
            }
        }
