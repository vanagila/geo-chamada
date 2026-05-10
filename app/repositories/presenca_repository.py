from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from sqlalchemy import func
from geoalchemy2.functions import ST_Distance
from app.models.Presenca import Presenca, PresencaStatus
from app.models.Chamada import Chamada
from app.models.Turma import Turma

class PresencaRepository:
    def __init__(self, db: Session):
        self.db = db

    def verificar_duplicidade(self, aluno_id: int, chamada_id: int) -> bool:
        return self.db.query(Presenca).filter(
            Presenca.aluno_id == aluno_id,
            Presenca.chamada_id == chamada_id
        ).first() is not None

    def calcular_distancia(self, ponto_aluno, ponto_professor, raio: float):
        result = self.db.query(
            ST_Distance(ponto_professor, ponto_aluno).label("distancia"),
            func.ST_DWithin(ponto_professor, ponto_aluno, raio).label("dentro")
        ).first()
        return result.distancia, result.dentro

    def create(self, presenca: Presenca) -> Presenca:
        self.db.add(presenca)
        self.db.commit()
        self.db.refresh(presenca)
        return presenca

    def get_by_chamada(self, chamada_id: int) -> List[Presenca]:
        return self.db.query(Presenca).filter(
            Presenca.chamada_id == chamada_id
        ).order_by(Presenca.data_registro).all()

    def historico_aluno(self, aluno_id: int) -> List[Presenca]:
        return self.db.query(Presenca).filter(
            Presenca.aluno_id == aluno_id
        ).order_by(Presenca.data_registro.desc()).all()

    def abonar(self, presenca_id: int, professor_id: int, motivo: str) -> Optional[Presenca]:
        presenca = self.db.query(Presenca).filter(Presenca.id == presenca_id).first()
        if presenca:
            presenca.status = PresencaStatus.ABONADA
            presenca.abonado_por_id = professor_id
            presenca.data_abono = datetime.utcnow()
            presenca.motivo_abono = motivo
            self.db.commit()
            self.db.refresh(presenca)
        return presenca

    def presencas_turma(self, turma_id: int, data_inicio: datetime | None = None, data_fim: datetime | None = None) -> List[Presenca]:
        query = self.db.query(Presenca).join(Chamada).filter(
            Chamada.turma_id == turma_id)

        if data_inicio:
            query = query.filter(Presenca.data_registro >= data_inicio.replace(hour=0, minute=0, second=0))
        if data_fim:
            query = query.filter(Presenca.data_registro <= data_fim.replace(hour=23, minute=59, second=59, microsecond=999999))
        return query.order_by(Presenca.data_registro).all()

    def historico_aluno_disciplina(self, aluno_id: int, disciplina_id: int, skip: int = 0, limit: int = 100) -> List[Presenca]:
        return (
            self.db.query(Presenca)
            .join(Chamada, Chamada.id == Presenca.chamada_id)
            .join(Turma, Turma.id == Chamada.turma_id)
            .filter(
                Presenca.aluno_id == aluno_id,
                Turma.disciplina_id == disciplina_id
            )
            .order_by(Chamada.data_abertura.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def presenca_automatica(self, aluno_id: int, chamada_id: int, status: str) -> Presenca:
        if status == "AUSENTE":
            status_enum = PresencaStatus.AUSENTE
        elif status == "PRESENTE":
            status_enum = PresencaStatus.PRESENTE
        else:
            status_enum = PresencaStatus.ABONADA

        presenca = Presenca(
            aluno_id=aluno_id,
            chamada_id=chamada_id,
            coordenadas_aluno=None,
            distancia_calculada=None,
            data_registro=datetime.utcnow(),
            status=status_enum
        )
        self.db.add(presenca)
        self.db.commit()
        self.db.refresh(presenca)
        return presenca
