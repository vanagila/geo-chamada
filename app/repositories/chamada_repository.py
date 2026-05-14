from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from app.models.Chamada import Chamada, ChamadaStatus
from app.schemas.chamada import ChamadaCreate
from app.utils.geo import GeoUtils

class ChamadaRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, chamada: Chamada) -> Chamada:
        self.db.add(chamada)
        self.db.commit()
        self.db.refresh(chamada)
        return chamada

    def get_by_id(self, chamada_id: int) -> Optional[Chamada]:
        return self.db.query(Chamada).filter(Chamada.id == chamada_id).first()

    def get_by_turma(self, turma_id: int, skip: int = 0, limit: int = 100) -> List[Chamada]:
        return self.db.query(Chamada).filter(Chamada.turma_id == turma_id).offset(skip).limit(limit).all()

    def get_by_professor(self, professor_id: int, skip: int = 0, limit: int = 100) -> List[Chamada]:
        return self.db.query(Chamada).filter(Chamada.professor_id == professor_id).offset(skip).limit(limit).all()
