from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from sqlalchemy import func
from geoalchemy2.functions import ST_Distance
from app.models.Presenca import Presenca
from app.models.Chamada import Chamada

class PresencaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_chamada(self, chamada_id: int) -> Optional[Chamada]:
        return self.db.query(Chamada).filter(
            Chamada.id == chamada_id).first()

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

    def get_historico_aluno(self, aluno_id: int) -> List[Presenca]:
        return self.db.query(Presenca).filter(
            Presenca.aluno_id == aluno_id
        ).order_by(Presenca.data_registro.desc()).all()

    def abonar(self, presenca: Presenca) -> Presenca:
        self.db.commit()
        self.db.refresh(presenca)
        return presenca

    def get_presencas_turma(self, turma_id: int, data_inicio: datetime = None, data_fim: datetime = None) -> List[Presenca]:
        query = self.db.query(Presenca).join(Chamada).filter(
            Chamada.turma_id == turma_id)

        if data_inicio:
            query = query.filter(Presenca.data_registro >= data_inicio)
        if data_fim:
            query = query.filter(Presenca.data_registro <= data_fim)

        return query.order_by(Presenca.data_registro).all()

    def get_presencas_chamada(self, chamada_id: int):
        return self.db.query(Presenca).filter(
            Presenca.chamada_id == chamada_id
        ).order_by(Presenca.data_registro).all()
