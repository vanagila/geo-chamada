from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.Disciplina import Disciplina
from app.models.Turma import Turma
from app.schemas.disciplina import DisciplinaCreate, DisciplinaUpdate

class DisciplinaRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, disciplina: Disciplina) -> Disciplina:
        self.db.add(disciplina)
        self.db.commit()
        self.db.refresh(disciplina)
        return disciplina

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Disciplina]:
        return self.db.query(Disciplina).offset(skip).limit(limit).all()

    def get_by_id(self, disciplina_id: int) -> Optional[Disciplina]:
        return self.db.query(Disciplina).filter(Disciplina.id == disciplina_id).first()

    def get_by_codigo(self, codigo: str) -> Optional[Disciplina]:
        return self.db.query(Disciplina).filter(Disciplina.codigo == codigo).first()

    def delete(self, disciplina: Disciplina) -> bool:
        self.db.delete(disciplina)
        self.db.commit()
        return True

    def count_turmas(self, disciplina_id: int) -> int:
        return self.db.query(Turma).filter(Turma.disciplina_id == disciplina_id).count()
