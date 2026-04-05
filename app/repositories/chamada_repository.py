from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from app.models.Chamada import Chamada, ChamadaStatus
from app.schemas.chamada import ChamadaCreate
from app.utils.geo import GeoUtils

class ChamadaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, chamada_data: ChamadaCreate, professor_id: int) -> Chamada:
        db_chamada = Chamada(
            turma_id=chamada_data.turma_id,
            professor_id=professor_id,
            coordenadas_professor=GeoUtils.criar_ponto(
                chamada_data.coordenadas.latitude,
                chamada_data.coordenadas.longitude
            ),
            raio=chamada_data.raio,
            data_abertura=datetime.utcnow(),
            status=ChamadaStatus.ABERTA
        )

        self.db.add(db_chamada)
        self.db.commit()
        self.db.refresh(db_chamada)
        return db_chamada

    def get_by_id(self, chamada_id: int) -> Optional[Chamada]:
        return self.db.query(Chamada).filter(Chamada.id == chamada_id).first()

    def get_by_turma(self, turma_id: int, skip: int = 0, limit: int = 100) -> List[Chamada]:
        return self.db.query(Chamada).filter(Chamada.turma_id == turma_id).offset(skip).limit(limit).all()

    def get_by_professor(self, professor_id: int, skip: int = 0, limit: int = 110) -> List[Chamada]:
        return self.db.query(Chamada).filter(Chamada.professor_id == professor_id).offset(skip).limit(limit).all()

    def encerrar(self, chamada_id: int) -> Optional[Chamada]:
        chamada = self.get_by_id(chamada_id)
        if chamada:
            chamada.status = ChamadaStatus.ENCERRADA
            chamada.data_encerramento = datetime.utcnow()
            self.db.commit()
            self.db.refresh(chamada)
        return chamada
