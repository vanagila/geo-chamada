from sqlalchemy.orm import Session
from typing import Optional, List, Tuple
from fastapi import HTTPException, status
from datetime import datetime
from app.models.Presenca import Presenca, PresencaStatus
from app.models.Usuario import Usuario
from app.models.Chamada import Chamada
from app.repositories.presenca_repository import PresencaRepository
from app.repositories.chamada_repository import ChamadaRepository
from app.repositories.disciplina_repository import DisciplinaRepository
from app.schemas.presenca import PresencaCreate, PresencaResponse, HistoricoAlunoDisciplinaResponse, EstatisticaResponse, DisciplinaResumo, AbonoResponse, AbonoDetailResponse
from app.utils.geo import GeoUtils
from app.utils.presenca_mapper import presenca_to_response

class PresencaService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = PresencaRepository(db)
        self.disciplina_repo = DisciplinaRepository(db)
        self.chamada_repo = ChamadaRepository(db)

    def marcar_presenca(self, aluno_id: int, presenca_data: PresencaCreate) -> Tuple[Presenca, bool]:
        chamada = self.chamada_repo.get_by_id(presenca_data.chamada_id)
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

    def abonar_ausencia(self, professor_id: int, presenca_id: int, motivo: str) -> AbonoResponse:
        presenca = self.db.query(Presenca).filter(
            Presenca.id == presenca_id).first()
        if not presenca:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Presença não encontrada"
            )

        if presenca.status == PresencaStatus.ABONADA:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Falta já abonada"
            )

        if presenca.status == PresencaStatus.PRESENTE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não é possível abonar uma presença já confirmada"
            )

        chamada = self.db.query(Chamada).filter(Chamada.id == presenca.chamada_id).first()
        if chamada and chamada.professor_id != professor_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você só pode abonar faltas das suas próprias chamadas"
            )

        presenca_atualizada = self.repository.abonar(
            presenca_id=presenca_id,
            professor_id=professor_id,
            motivo=motivo
        )

        if not presenca_atualizada:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao abonar falta"
            )

        return AbonoResponse(
            message="Falta abonada com sucesso",
            presenca=AbonoDetailResponse(
                id=presenca.id,
                aluno_id=presenca.aluno_id,
                chamada_id=presenca.chamada_id,
                status=presenca.status.value,
                distancia_calculada=presenca.distancia_calculada,
                data_registro=presenca.data_registro,
                abonado_por_id=professor_id,
                data_abono=presenca.data_abono,
                motivo_abono=presenca.motivo_abono
            )
        )

    def presencas_turma(self, turma_id: int, data_inicio: datetime | None = None, data_fim: datetime | None = None) -> List[dict]:
        presencas = self.repository.presencas_turma(turma_id, data_inicio, data_fim)
        if not presencas:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhuma presença encontrada"
            )
        return [presenca_to_response(p) for p in presencas]

    def historico_aluno(self, aluno_id: int) -> List[Presenca]:
        presencas = self.repository.historico_aluno(aluno_id)
        return [presenca_to_response(p) for p in presencas]

    def historico_aluno_disciplina(self, aluno_id: int, disciplina_id: int) -> HistoricoAlunoDisciplinaResponse:
        disciplina = self.disciplina_repo.get_by_id(disciplina_id)
        if not disciplina:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Disciplina não encontrada"
            )

        presencas = self.repository.historico_aluno_disciplina(aluno_id, disciplina_id)
        presencas_serializaveis = [presenca_to_response(p) for p in presencas]
        return HistoricoAlunoDisciplinaResponse(
            disciplina=DisciplinaResumo(
                id=disciplina.id,
                nome=disciplina.nome,
                codigo=disciplina.codigo
            ),
            presencas=presencas_serializaveis,
            estatisticas=EstatisticaResponse(
                total=len(presencas),
                presentes=sum(1 for p in presencas if p.status.value == "PRESENTE"),
                ausentes=sum(1 for p in presencas if p.status.value == "AUSENTE"),
                abonadas=sum(1 for p in presencas if p.status.value == "ABONADA")
            )
        )

    def presencas_chamada(self, chamada_id: int) -> List[PresencaResponse]:
        presencas = self.repository.get_by_chamada(chamada_id)
        return [presenca_to_response(p) for p in presencas]
