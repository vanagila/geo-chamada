from sqlalchemy.orm import Session
from typing import Optional, List, Tuple
from fastapi import HTTPException, status
from datetime import datetime
from app.models.Presenca import Presenca, PresencaStatus
from app.models.Usuario import Usuario
from app.repositories.presenca_repository import PresencaRepository
from app.schemas.presenca import PresencaCreate, PresencaResponse
from app.utils.geo import GeoUtils

class PresencaService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = PresencaRepository(db)

    def marcar_presenca(self, aluno_id: int, presenca_data: PresencaCreate) -> Tuple[Presenca, bool]:
        chamada = self.repository.get_chamada(presenca_data.chamada_id)
        if not chamada:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chamada não encontrada"
            )

        if chamada.status != "ABERTA":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Chamada encerrada"
            )

        aluno = self.db.query(Usuario).filter(
            Usuario.id == aluno_id).first()
        if not aluno:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aluno não encontrado"
            )

        if not any(a.id == aluno_id for a in chamada.turma.alunos):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aluno não pertence à turma"
            )

        if self.repository.verificar_duplicidade(aluno_id, presenca_data.chamada_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Presença já registrada"
            )

        latitude = presenca_data.coordenadas.latitude
        longitude = presenca_data.coordenadas.longitude
        if not GeoUtils.validar_coordenadas(latitude, longitude):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Coordenadas inválidas"
            )

        ponto = GeoUtils.criar_ponto(latitude, longitude)

        distancia, dentro = self.repository.calcular_distancia(
            ponto,
            chamada.coordenadas_professor,
            chamada.raio
        )

        situacao_presenca = (
            PresencaStatus.PRESENTE
            if dentro
            else PresencaStatus.AUSENTE
        )

        presenca = Presenca(
            aluno_id=aluno_id,
            chamada_id=presenca_data.chamada_id,
            coordenadas_aluno=ponto,
            distancia_calculada=distancia,
            status=situacao_presenca,
            data_registro=datetime.utcnow()
        )

        presenca = self.repository.create(presenca)
        return presenca, dentro

    def abonar_ausencia(self, professor_id: int, presenca_id: int, motivo: str) -> Presenca:
        presenca = self.db.query(Presenca).filter(
            Presenca.id == presenca_id).first()
        if not presenca:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Presença não encontrada"
            )
        presenca.status = PresencaStatus.ABONADA
        presenca.abonado_por_id = professor_id
        presenca.data_abono = datetime.utcnow()
        presenca.motivo_abono = motivo
        return self.repository.abonar(presenca)

    def historico_aluno(self, aluno_id: int) -> List[Presenca]:
        presencas = self.repository.get_historico_aluno(aluno_id)
        return [self._to_response(p) for p in presencas]

    def presencas_chamada(self, chamada_id: int) -> List[PresencaResponse]:
        presencas = self.repository.get_presencas_chamada(chamada_id)
        return [self._to_response(p) for p in presencas]

    def _to_response(self, p: Presenca) -> PresencaResponse:
        dentro_raio = (
            p.distancia_calculada is not None and
            p.chamada is not None and
            p.distancia_calculada <= p.chamada.raio
        )
        return PresencaResponse(
            id=p.id,
            aluno_id=p.aluno_id,
            chamada_id=p.chamada_id,
            distancia_calculada=p.distancia_calculada,
            data_registro=p.data_registro,
            status=p.status,
            dentro_raio=dentro_raio
        )
